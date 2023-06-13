from asyncio import sleep
import datetime
import json
import time
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
            response = json.loads(self.zdocs.invoke_api('/bundlelist?rpp=100&page='+str(page)+labelkeys_query_param, 'GET').content)
            for bundle in response['bundle_list']:
                bundle_list.append(bundle)
            if response['pagination_data']['next_page']!=None:
                page = page + 1
            else:
                page = -1    
        return bundle_list  
    
    def get_all_bundles_admin(self):
        publications = self.get_all_publications_admin()
        resources= self.get_all_resources_admin()
        for resource in resources:
            publications.append(resource)
        return publications
    
    def get_all_publications_or_resources_admin(self, url):
        response = self.zdocs.invoke_api(url,'GET',{},False,False)
        soup = BeautifulSoup(response.content)
        a_tags = soup.find_all('a', {'class': 'dropdown-item post pointer link-download'})
        bundle_list = []
        for a_tag in a_tags:
            bundle_url=a_tag.get('url')
            i = bundle_url.index('/bundle/')
            bundle_name = bundle_url[i+len('/bundle/'):][:-len('/reindex')]
            bundle_list.append(bundle_name)
        return bundle_list

    def get_all_publications_admin(self):   
        max_number_of_bundles= 10000 
        bundle_list = self.get_all_publications_or_resources_admin(self.zdocs.base_url+'/admin/managebundles?rpp='+str(max_number_of_bundles))
        return bundle_list

    def get_all_resources_admin(self):
        max_number_of_bundles= 10000
        bundle_list = self.get_all_publications_or_resources_admin(self.zdocs.base_url+'/admin/manageresourcebundles?rpp='+str(max_number_of_bundles))
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
        print(str(len(already_indexed_bundles))+' out of '+str(len(bundles_to_be_indexed))+' are already indexed')
        counter = 0
        wait_for_empty_queue_after_x_bundles = 1
        sleep_time_between_empty_queue_checks = 60
        bundles_indexed = []
        for bundle in bundles_to_be_indexed:
            print('checking bundle '+bundle)
            if counter==wait_for_empty_queue_after_x_bundles:
                while not(self.indexing_queue_empty()):
                    time.sleep(sleep_time_between_empty_queue_checks) 
                    thetime = time.localtime()
                    current_time = time.strftime("%H:%M:%S", thetime)
                    print(current_time+' waiting for indexing queue to clear..')
                counter=0 
            else:         
                counter+=1 
            reindexing_required = True    
            if do_not_reindex_already_indexed_bundles:    
                reindexing_required = not(self.bundle_already_indexed(already_indexed_bundles, bundle)) 
            if reindexing_required:  
                response =  self.zdocs.invoke_api(self.zdocs.base_url+'/bundle/'+bundle+'/reindex','POST',[],True,False).status_code     
                print('reindexing bundle '+bundle)
                print(response)
                bundles_indexed.append(bundle) 
            else:
                print('bundle '+bundle+' is already indexed')                                     
        return bundles_indexed

    def indexing_queue_empty(self):
         response =  json.loads(self.zdocs.invoke_api('/admin/reindex/status','GET').content)
         #print (response['queue'])
         print('there are currently '+str(len(response['queue']))+' bundles in the queue')
         return len(response['queue'])==0
    
    def bundle_already_indexed(self,bundle_list:list, bundle_name):
        #print ('checking if '+ bundle_name+ ' is already indexed')
        #print('bundle_list', len(bundle_list))
        for bundle in bundle_list:
            #print(bundle['name'])
            if bundle['name'] == bundle_name:
                return True
        return False
        


