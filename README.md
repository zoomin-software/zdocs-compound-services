# Install:
pip3 install requests
pip3 install bs4
pip3 install datetime

# Configuration: 
1. generate a Zoomin API key,secret as explianed here - https://docs.zoominsoftware.io/bundle/api-auth/page/workflow__authenticate_to_zoomin_api_with_access_keys.html
2.create client configuration file: use templates/client_config.json as template 


# To test "get_all_attachments"
   - Run: e.g to get all attachments of bundles taged as "kb" using configuration file client_config.json and export the reuslts into the file client_attachments.json, cd into the "test" folder, and run this command - 
    python3 attachments_test.py client_config.json "kb" client_attachments.json
