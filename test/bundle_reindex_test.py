import json
import sys


sys.path.insert(0, '../src')
from login import ZdocsLogin
from bundle import Bundle

# parameters:
# 1) config file name
# 2) list of labels keys to filter the bundles form which the attachments shall be returned e.g "kb, dita"
# 3) output file name
# E.g attachments_test.py acme_config.json ['kb'] acme_attachments.json
if __name__ == "__main__":
    config_file = open(sys.argv[1], "r")
    config = json.load(config_file) 
    base_url = config['domain']+'/api'
    zdocs = ZdocsLogin(base_url,config['key'],config['secret'],config['cookie'])

    bundle = Bundle(zdocs)
    bundle.reindex_all_bundles()
