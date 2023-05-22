import json
import string
import sys
import xmltodict

sys.path.insert(0, '../src')

from bundle import Bundle
from login import ZdocsLogin


#parameters: 
#1) config file name
#2) list of labels keys to filter the bundles form which the attachments shall be returned e.g "kb, dita"
#3) output file name
#E.g attachments_test.py acme_config.json ['kb'] acme_attachments.json 
if __name__ == "__main__":
     
    file = open(sys.argv[1], "r")
    config = json.load(file) 
    zdocs = ZdocsLogin(config['domain'],config['key'],config['secret'])

    filelist_path = sys.argv[2]
    filelist_path_json = 'filelist'

    with open(filelist_path) as xml_file:
        data_dict = xmltodict.parse(xml_file.read())
        json_data = json.dumps(data_dict)
        with open(filelist_path_json, "w") as json_file:
            json_file.write(json_data)
        file = open(filelist_path_json, "r")
        pint = json.load(file) 

        pint_topics = []
        for i in pint['files']['file']:
            pint_topics.append(i['@relpath'])

    bundle = Bundle(zdocs)
    existing_topics = bundle.topic_exists(sys.argv[3],pint_topics)
     


