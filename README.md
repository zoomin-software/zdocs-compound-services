# zdocs-compound-services

To test "get_all_attachments":
   - generate a key,secret as expa,olhe here - https://docs.zoominsoftware.io/bundle/api-auth/page/workflow__authenticate_to_zoomin_api_with_access_keys.html
   - clone this repo 
   - create client configuration file: use templates/client_config.json as template 
   - Run e.g to get all attachments of bundles taged as "kb" using configuration file client_config.json and export the reuslts into the file client_attachments.json:
    python3 attachments_test.py client_config.json "kb" client_attachments.json
