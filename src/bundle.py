import json
from login import ZdocsLogin

class Bundle:
    def __new__(cls,zdocs: ZdocsLogin):
        Bundle.zdocs = zdocs
        return super().__new__(cls)

    def get_all_bundles(self, labelkeys: list):
        print (labelkeys)
        labelkeys_query_param = self.zdocs.to_labelkeys_query_param(labelkeys)
        print (labelkeys_query_param)
        return json.loads(self.zdocs.invoke_api('/bundlelist?'+labelkeys_query_param, 'GET').content)['bundle_list']
  
    def get_bundle_topics(self,bundle):
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
        response = {"existing": existing_topics, "non_exisitng":nonexisting_topics, "duplicates":duplicate_topics} 
        print(response["duplicates"])
        print(len(response["existing"]),len(response["non_exisitng"]),response["non_exisitng"])
        return response

    def number_of_topics(self,bundle): 
        return len(self.get_bundle_topics(bundle))
    
    def delete_bundles(self,bundles):
        for bundle in bundles:
           json.loads(self.zdocs.invoke_api('/bundle/'+bundle, 'DELETE').content)