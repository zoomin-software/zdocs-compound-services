import json
import sys
import login
from bundle import Bundle
from topic import Topic

class Attachment:
    def __new__(cls,config_file_name):
        file = open(config_file_name, "r")
        config = json.load(file) 
        cls.base_url = config['domain']+'/api'
        cls.zdocs = login.ZdocsLogin(cls.base_url,config['key'],config['secret'])
        cls.bundle =  Bundle(cls.zdocs)
        cls.topic =  Topic(cls.zdocs)
        return super().__new__(cls)

    def get_all_attachments(self):
        all_attachments = []
        #call bundlelist to get all bundles
        bundles = self.bundle.get_all_bundles(['kb'])

        #for each bundle get all topics
        for bundle in bundles:
            topics = self.bundle.get_bundle_topics(bundle['name'])

            #for each topic get topic attachments 
            for topic in topics:
                attachments = self.topic.get_topic_attachments(bundle['name'],topic)
                for attachment in attachments:
                    if attachment:
                        all_attachments.append(attachment)
        return all_attachments