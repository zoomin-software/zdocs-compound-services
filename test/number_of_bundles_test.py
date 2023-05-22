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
    base_url = config['domain']+'/api'
    zdocs = ZdocsLogin(base_url,config['key'],config['secret'])

    bundle = Bundle(zdocs)
    print(bundle.number_of_topics(sys.argv[2]))
     


