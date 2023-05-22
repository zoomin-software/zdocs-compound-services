import json
from login import ZdocsLogin


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
            
    def get_bundle_topics(self, bundle):
        return json.loads(self.zdocs.invoke_api('/bundle/'+bundle+'/pages', 'GET').content)

    def topic_exists(self, bundle, topic_names):
        #print(len(topic_names))
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

    def reindex_all_bundles(self):
        bundles = self.get_all_bundles([])
        print(bundles[0])
        for bundle in bundles:
           print(bundle['name'])
           response =  self.zdocs.invoke_api(self.zdocs.base_url+'/bundle/'+bundle['name']+'/reindex','POST',[],True,False).status_code
           print(response)
        return len(bundles)
