import json
import string
import sys

sys.path.insert(0, '../src')
from bundle import Bundle
from login import ZdocsLogin

#parameters: 
#1) config file name
if __name__ == "__main__":
    file = open(sys.argv[1], "r")
    config = json.load(file) 
    zdocs = ZdocsLogin(config['domain'],config['key'],config['secret'])
    bundle = Bundle(zdocs)
    bundle.get_all_bundles_admin()


