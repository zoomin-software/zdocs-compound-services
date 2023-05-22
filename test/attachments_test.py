import json
import string
import sys

sys.path.insert(0, '../src')
from attachment import Attachment
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
    zdocs_attachment = Attachment(zdocs)
    labelkeys = list(sys.argv[2].split(","))
    all_attachments = zdocs_attachment.get_all_attachments(labelkeys)
    with open(sys.argv[3], 'w') as f:
        data = {"name": "attachments"}
        json.dump(all_attachments, f)


