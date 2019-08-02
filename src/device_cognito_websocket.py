#!/usr/bin/env python
# -*- coding: utf-8 -*-

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json
import time
import sys
import boto3
import requests
import argparse

#获取参数
parser = argparse.ArgumentParser(description='Send data to IoT Core')
parser.add_argument('--iot_policy_name', default="IoTPolicyForDeviceCognitoWebsocket",
            help='iot policy name for device_cognito_websocket.')
parser.add_argument('--developer_provicer_endpoint', default="http://127.0.0.1:8383/login/",
            help='developer ID provider endpoint')
parser.add_argument('--endpoint_prefix', required=True,
            help='your iot endpoint prefix.')

args = parser.parse_args()
policy_name = args.iot_policy_name
developer_provicer_endpoint = args.developer_provicer_endpoint
endpoint_prefix = args.endpoint_prefix

device_name = 'device_cognito_websocket'
region = 'cn-north-1'

private_topic = "IoTDemo/"+device_name

server_root_ca_file = "./AmazonRootCA1.pem"

endpoint = "%s.ats.iot.cn-north-1.amazonaws.com.cn" % endpoint_prefix
port = 443

headers = {"Content-Type": "application/json"}
body = {"device_id":device_name}
r1 = requests.post(developer_provicer_endpoint, data=json.dumps(body), headers = headers)

token = json.loads(r1.text)['token']
identityId = json.loads(r1.text)['identityId']

cognito_client = boto3.client('cognito-identity', region_name=region)
response = cognito_client.get_credentials_for_identity(IdentityId=identityId, Logins={'cognito-identity.cn-north-1.amazonaws.com.cn':token})

sessionToken=response['Credentials']['SessionToken']
accessKeyId=response['Credentials']['AccessKeyId']
secretKey=response['Credentials']['SecretKey']

iot_client = boto3.client('iot',region_name=region,aws_access_key_id=accessKeyId,aws_secret_access_key=secretKey,aws_session_token=sessionToken)

response = iot_client.attach_policy(
    policyName=policy_name,
    target=identityId
)

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
    myAWSIoTMQTTClient.configureIAMCredentials(accessKeyId, secretKey, sessionToken)

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
