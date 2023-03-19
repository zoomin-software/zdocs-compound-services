import json
from login import ZdocsLogin

class Topic:
    attachments = []
    def __new__(cls,zdocs: ZdocsLogin):
        Topic.zdocs = zdocs
        return super().__new__(cls)

    def get_topic_attachments(self,bundle,topic):
        return json.loads(self.zdocs.invoke_api('/bundle/'+bundle+'/page/'+topic, 'GET').content)['attachments']['topic_attachments']
    

 