#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os

#获取参数
parser = argparse.ArgumentParser(description='Send data to IoT Core')
parser.add_argument('--data', default="data from device x509 http",
            help='data to IoT')
parser.add_argument('--endpoint_prefix', required=True,
            help='your iot endpoint prefix.')
parser.add_argument('--client_cert', required=True,
            help='your client cert file.')
parser.add_argument('--client_key', required=True,
            help='your client key file.')

args = parser.parse_args()
private_data = args.data
endpoint_prefix = args.endpoint_prefix
client_cert = args.client_cert
client_key = args.client_key

device_name = 'device_x509_http'
region = 'cn-north-1'
private_topic = "IoTDemo/"+device_name

server_root_ca_file = "./AmazonRootCA1.pem"
client_cert_file = "./%s" % client_cert
client_key_file = "./%s" % client_key

#port 8444. 443需要支持ALPN
iot_endpoint = "https://%s.ats.iot.cn-north-1.amazonaws.com.cn:8443/topics/" % endpoint_prefix

data = "{\\\"source\\\":\\\"%s\\\", \\\"data\\\":\\\"%s\\\"}" % (device_name, private_data)
endpoint = iot_endpoint + private_topic
command = "curl --tlsv1.2 --cacert %s --cert %s --key %s -X POST -d \"%s\" %s" % (server_root_ca_file,client_cert_file,client_key_file,data,endpoint)
#print command
os.system(command)
