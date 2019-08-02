#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import json
import requests
import commands
import base64

#获取参数
parser = argparse.ArgumentParser(description='Send data to IoT Core')
parser.add_argument('--data', default="data from device_custom_auth_http.",
            help='data to IoT')
parser.add_argument('--authorizer_name', required=True,
            help='custom authorizer name.')
parser.add_argument('--endpoint_prefix', required=True,
            help='your iot endpoint prefix.')
parser.add_argument('--private_key', required=True,
            help='your custom authorizer private key.')

args = parser.parse_args()
private_data = args.data
endpoint_prefix = args.endpoint_prefix
authorizer_name = args.authorizer_name
private_key = args.private_key

device_name = 'device_custom_auth_http'
region = 'cn-north-1'
private_topic = "IoTDemo/"+device_name

iot_endpoint = "https://%s.iot.cn-north-1.amazonaws.com.cn/topics/" % endpoint_prefix

token = {"device_id":device_name}
token_str = base64.b64encode(json.dumps(token))

command = "/bin/echo -n %s | openssl dgst -sha256 -sign %s 2>/dev/null| openssl base64 2>/dev/null" % (token_str,private_key)

return_code, return_str = commands.getstatusoutput(command)
signature = return_str.strip().replace('\n','')
headers = {
    "Content-Type": "application/json",
    "IoTDemoAuthorizerToken":token_str,
    "X-Amz-CustomAuthorizer-Signature":signature,
    "X-Amz-CustomAuthorizer-Name":authorizer_name
}
data = json.dumps({"source":device_name, "data":private_data})
endpoint = iot_endpoint + private_topic
r1 = requests.post(endpoint, data=data, headers = headers)
