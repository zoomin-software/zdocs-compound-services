import json
import sys
import login
from bundle import Bundle
from topic import Topic

class Attachment:
    def __new__(cls,zdocs: login.ZdocsLogin):
        cls.zdocs = zdocs
        cls.bundle =  Bundle(cls.zdocs)
        cls.topic =  Topic(cls.zdocs)
        return super().__new__(cls)

    def get_all_attachments(self, labelkeys):
        all_attachments = []
        #call bundlelist to get all bundles
        bundles = self.bundle.get_all_bundles(labelkeys)
        print(bundles)
        #for each bundle get all topics
        for bundle in bundles:
            topics = self.bundle.get_bundle_topics(bundle['name'])
            #for each topic get topic attachments 
            for topic in topics:
                print(topic)
                attachments = self.topic.get_topic_attachments(bundle['name'],topic)
                if attachments:
                    topic_attachments = {"topic_name": topic, "bundle": bundle['name'],
                         "attachments": attachments}
                    #print(topic_attachments)
                    # for attachment in attachments:
                    #     if attachment:
                    all_attachments.append(topic_attachments)
        return all_attachments