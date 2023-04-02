import json
import string
import sys
sys.path.insert(0, '../src')
from attachment import Attachment

#parameters: 
#1) config file name
#2) list of labels keys to filter the bundles form which the attachments shall be returned e.g "kb, dita"
#3) output file name
#E.g attachments_test.py acme_config.json ['kb'] acme_attachments.json 
if __name__ == "__main__":
    
    zdocs_attachment = Attachment(sys.argv[1])
    labelkeys = list(sys.argv[2].split(","))
    all_attachments = zdocs_attachment.get_all_attachments(labelkeys)
    with open(sys.argv[3], 'w') as f:
        data = {"name": "attachments"}
        json.dump(all_attachments, f)


