import json
from login import ZdocsLogin

class Bundle:
    def __new__(cls,zdocs: ZdocsLogin):
        Bundle.zdocs = zdocs
        return super().__new__(cls)

    def get_all_bundles(self, labelkeys: list):
        print (labelkeys)
        labelkeys_query_param = self.zdocs.to_labelkeys_query_param(labelkeys)
        return json.loads(self.zdocs.invoke_api('/bundlelist?'+labelkeys_query_param, 'GET').content)['bundle_list']
  
    def get_bundle_topics(self,bundle):
        return json.loads(self.zdocs.invoke_api('/bundle/'+bundle+'/pages', 'GET').content)