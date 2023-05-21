import sys
sys.path.insert(0, '../src')

from bundle import Bundle

# parameters:
# 1) config file name
# 2) list of labels keys to filter the bundles form which the attachments shall be returned e.g "kb, dita"
# 3) output file name
# E.g attachments_test.py acme_config.json ['kb'] acme_attachments.json
if __name__ == "__main__":

    zdocs_bundle = Bundle(sys.argv[0])
    zdocs_bundle.reindex_all_bundles()
