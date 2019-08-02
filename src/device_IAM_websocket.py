#!/usr/bin/env python
# -*- coding: utf-8 -*-

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json
import time
import sys
import argparse

parser = argparse.ArgumentParser(description='Send data to IoT Core')
parser.add_argument('--endpoint_prefix', required=True,
            help='endpoint prefix')
parser.add_argument('--AccessKeyId', required=True,
            help='AccessKeyId')
parser.add_argument('--SecretAccessKey', required=True,
            help='SecretAccessKey')

args = parser.parse_args()
endpoint_prefix = args.endpoint_prefix
access_key_id = args.AccessKeyId
secret_access_key = args.SecretAccessKey

device_name = 'device_IAM_websocket'
region = 'cn-north-1'
private_topic = "IoTDemo/"+device_name

base_path = "."
server_root_ca_file = base_path + "/AmazonRootCA1.pem"

endpoint = "%s.ats.iot.cn-north-1.amazonaws.com.cn" % endpoint_prefix
port = 443

# Custom MQTT message callback
def customCallback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")

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
            myAWSIoTMQTTClient.publish(private_topic, messageJson, 1)
            pri_loopCount += 1
            time.sleep(2)
    except:
        sys.exit()

if __name__ == '__main__':
    # Init AWSIoTMQTTClient
    myAWSIoTMQTTClient = None
    myAWSIoTMQTTClient = AWSIoTMQTTClient(device_name, useWebsocket=True)
    myAWSIoTMQTTClient.configureEndpoint(endpoint, port)
    myAWSIoTMQTTClient.configureCredentials(server_root_ca_file)
    myAWSIoTMQTTClient.configureIAMCredentials(access_key_id, secret_access_key)

    # AWSIoTMQTTClient connection configuration
    myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
    myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
    myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
    myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
    myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

    # Connect and subscribe to AWS IoT
    myAWSIoTMQTTClient.connect()
    myAWSIoTMQTTClient.subscribe(private_topic, 1, customCallback)
    time.sleep(2)

    pub_msg()
