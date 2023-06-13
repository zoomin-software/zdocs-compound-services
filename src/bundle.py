from asyncio import sleep
import datetime
import json
from login import ZdocsLogin
from bs4 import BeautifulSoup
from datetime import datetime

class Bundle:
    def __new__(cls, zdocs: ZdocsLogin):
        Bundle.zdocs = zdocs
        return super().__new__(cls)

    def get_all_bundles(self, labelkeys: list):
        #print(labelkeys)
        labelkeys_query_param = self.zdocs.to_labelkeys_query_param(labelkeys)
        #print(labelkeys_query_param)
        page = 1      
        bundle_list = []
        while page>0:
            response = json.loads(self.zdocs.invoke_api('/bundlelist?page='+str(page)+labelkeys_query_param, 'GET').content)
            for bundle in response['bundle_list']:
                bundle_list.append(bundle)
            if response['pagination_data']['next_page']!=None:
                page = page + 1
            else:
                page = -1    
        return bundle_list  

    def get_all_bundles_admin(self):
        response = self.zdocs.invoke_api(self.zdocs.base_url+'/admin/managebundles?rpp=10000','GET',{},False,False)
        soup = BeautifulSoup(response.content)
        a_tags = soup.find_all('a', {'class': 'dropdown-item post pointer link-download'})
        bundle_list = []
        for a_tag in a_tags:
            bundle_url=a_tag.get('url')
            i = bundle_url.index('/bundle/')
            bundle_name = bundle_url[i+len('/bundle/'):][:-len('/reindex')]
            bundle_list.append(bundle_name)
        return bundle_list
           
            
    def get_bundle_topics(self, bundle):
        return json.loads(self.zdocs.invoke_api('/bundle/'+bundle+'/pages', 'GET').content)

    #there are cases where there a topic on PINT side that are not known by Zdocs, and full reindex won't solve it
    #could happen because of unrecognized labels for examples
    #this method returns these topics which are in "topics_names" but not in the bundle page 
    def topic_exists(self,bundle, topic_names):
        existing_topics = set()
        nonexisting_topics = set()
        duplicate_topics = set()
        indexed_topics = self.get_bundle_topics(bundle)
        for topic in topic_names:
            if topic in indexed_topics:
                if topic in existing_topics:
                    duplicate_topics.add(topic)
                else:
                    existing_topics.add(topic)
            else:
                nonexisting_topics.add(topic)
        response = {"exiting": existing_topics,
                    "non_exisitng": nonexisting_topics, "duplicates": duplicate_topics}
        #(response["duplicates"])
        #print(len(response["non_exisitng"]), response["non_exisitng"])
        return response
    
    def number_of_topics(self,bundle): 
        return len(self.get_bundle_topics(bundle))
    
    def delete_bundles(self,bundles):
        for bundle in bundles:
           json.loads(self.zdocs.invoke_api('/bundle/'+bundle, 'DELETE').content)

    def reindex_all_bundles(self,do_not_reindex_already_indexed_bundles=True):
        already_indexed_bundles = self.get_all_bundles([])
        bundles_to_be_indexed = self.get_all_bundles_admin()
        counter = 0
        wait_for_empty_queue_after_x_bundles = 2
        sleep_time_between_empty_queue_checks = 60
        bundles_indexed = []
        for bundle in bundles_to_be_indexed:
            print(bundle)
            if counter==wait_for_empty_queue_after_x_bundles:
                while not(self.indexing_queue_empty()):
                    sleep(sleep_time_between_empty_queue_checks) 
                    time = time.localtime()
                    current_time = time.strftime("%H:%M:%S", t)
                    print(current_time+' waiting for indexing queue to clear..')
                counter=0 
            else:         
                counter+=1 
            reindexing_required = True    
            if do_not_reindex_already_indexed_bundles:    
                reindexing_required = not(self.bundle_already_indexed(already_indexed_bundles, bundle)) 
            if reindexing_required:  
                response =  self.zdocs.invoke_api(self.zdocs.base_url+'/bundle/'+bundle+'/reindex','POST',[],True,False).status_code     
                print(response)
                bundles_indexed.append(bundle)                                  
        return bundles_indexed

    def indexing_queue_empty(self):
         response =  json.loads(self.zdocs.invoke_api('/admin/reindex/status','GET').content)
         print (response['queue'])
         return len(response['queue'])==0
    
    def bundle_already_indexed(self,bundle_list:list, bundle_name):
        print (bundle_name)
        for bundle in bundle_list:
            print(bundle['name'])
            if bundle['name'] == bundle_name:
                print('bundle '+bundle_name+ ' is already indexed')
                return True
        return False
        


