import json
import sys
sys.path.insert(0, '../src')
from attachment import Attachment

#main
if __name__ == "__main__":
    zdocs_attachment = Attachment(sys.argv[1])
    all_attachments = zdocs_attachment.get_all_attachments()
    with open('kofax_attachments.json', 'w') as f:
        data = {"name": "attachments"}
        json.dump(all_attachments, f)


