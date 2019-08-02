#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import commands
import sys
import argparse
import base64
import time

from paho.mqtt.client import Client
import threading

#获取参数
parser = argparse.ArgumentParser(description='Send data to IoT Core')
parser.add_argument('--authorizer_name', required=True,
            help='custom authorizer name.')
parser.add_argument('--endpoint_prefix', required=True,
            help='your iot endpoint prefix.')
parser.add_argument('--private_key', required=True,
            help='your custom authorizer private key.')

args = parser.parse_args()
authorizer_name = args.authorizer_name
endpoint_prefix = args.endpoint_prefix
private_key = args.private_key

device_name = 'device_custom_auth_websocket'
region = 'cn-north-1'
private_topic = "IoTDemo/"+device_name

iot_endpoint = "%s.iot.cn-north-1.amazonaws.com.cn" % endpoint_prefix  #ATS不支持！！！！！
ca_certs_file = "./VeriSign-Class 3-Public-Primary-Certification-Authority-G5.pem"
#ca_certs_file = "./AmazonRootCA1.pem"
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    #print("Connected with result code "+str(rc))
    client.subscribe(private_topic)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print("receive message from topic "+msg.topic+", message is "+str(msg.payload))

# This is specific to custom authorizer setup
token = {"device_id":device_name}
token_str = base64.b64encode(json.dumps(token))

command = "/bin/echo -n %s | openssl dgst -sha256 -sign %s 2>/dev/null| openssl base64 2>/dev/null" % (token_str,private_key)

return_code, return_str = commands.getstatusoutput(command)
signature = return_str.strip().replace('\n','')
aws_headers = {
    "IoTDemoAuthorizerToken":token_str,
    "X-Amz-CustomAuthorizer-Signature":signature,
    "X-Amz-CustomAuthorizer-Name":authorizer_name
}
client = Client(device_name, transport="websockets")
client.ws_set_options(headers=aws_headers)
client.tls_set(ca_certs = ca_certs_file)
client.on_connect = on_connect
client.on_message = on_message
client.connect(iot_endpoint, 443, 60)

def pub_msg():
    try:
        pri_loopCount = 0
        while True:
            print 'please input:',
            msg = raw_input()
            private_data = msg
            message = {}
            message['message'] = json.dumps({"source":device_name, "data":private_data})
            message['sequence'] = pri_loopCount
            messageJson = json.dumps(message)
            client.publish(private_topic, messageJson, 1)
            pri_loopCount += 1
            time.sleep(2)
    except:
        sys.exit()

t = threading.Thread(target=client.loop_forever,args=())
t.setDaemon(True)
t.start()
pub_msg()
