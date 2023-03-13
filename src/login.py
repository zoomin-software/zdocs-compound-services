# -*- coding: utf-8 -*-
"""
Utility methods and CLI tool for Zoomin API
When running from CLI use:
    python zd-client.py https://api-host.com --access your_access_key --secret your_secret
You can also use it as a library by calling  method `invoke_api`
"""
import requests
import hmac
import hashlib
import base64
import os
import sys
import urllib.parse
import json
import argparse
import calendar
import time

class ZdocsLogin:
	
    # methods
	

    def __new__(cls,base_url,api_access_key,api_secret):
        cls.api_access_key = api_access_key
        cls.api_secret = api_secret
        cls.base_url = base_url
        return super().__new__(cls)

    def do_request(self, verb, url, params, body, filename):
        """
        Performs the actual HTTP call
        """
        form_data = None
        result = requests.request(
            verb.lower(),
            url,
            params=params,
            headers={"Accept": "application/json",
                    "Content-Type": "application/json"},
            data=json.dumps(body),
            # files=form_data
        )
        return result
    
    def generate_signature(self, original_string, secret):
        """
        Generates SHA256 signature for the provided string and secret
        """
        original_string_bytes = original_string.encode(
            encoding='utf-8', errors='strict')
        # sign and endcode for passing in URL
        digest = hmac.new(
            secret.encode(encoding='utf-8', errors='strict'),
            msg=original_string_bytes,
            digestmod=hashlib.sha256).digest()
        digest_encoded = base64.urlsafe_b64encode(digest)
        return str(digest_encoded, encoding='utf8', errors='strict').rstrip('=')
    
    def invoke_api(self, endpoint_url, verb='GET', body=None, filename=None):
        """
        Performs Zoomin API call
        """
        url = self.base_url+endpoint_url
        print (url)
        assert url, "'url' is required"
        assert self.api_access_key, "'api_access_key' is required"
        assert self.api_secret, "'api_secret' is required"
        parsed_url = urllib.parse.urlsplit(url)
        #print(parsed_url)
        url_query_less = urllib.parse.urlunsplit(
            (parsed_url.scheme, parsed_url.hostname, parsed_url.path, '', ''))
        #print (url_query_less)    
        query = urllib.parse.parse_qs(parsed_url.query)
        # append timestamp to original Url
        timestamp = int(time.time())
        query.update({"timestamp": timestamp})
        # append signature
        #print ('url_query_less'+url_query_less)
        signature = self.generate_signature('%s?%s' % (
            url_query_less, urllib.parse.urlencode(query, doseq=True)), self.api_secret)
        query.update({"signature": signature})
        # append access key
        query.update({"accessKey": self.api_access_key})
        print(f"\n{url_query_less}?accessKey={self.api_access_key}&timestamp={timestamp}&signature={signature}")
        return self.do_request(verb, url_query_less, query, body, filename)

    def to_labelkeys_query_param(self, labelkeys:list):
        labelkeys.insert(0,'')
        labelkeys_query_param = ''
        if labelkeys:
            labelkeys_query_param = ('&labelkey='.join(labelkeys))[1:]
            print (labelkeys_query_param) 
        return labelkeys_query_param


