#coding:utf-8

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json
import time
import sys
import commands
import boto3
import argparse

parser = argparse.ArgumentParser(description='Send data to IoT Core')
parser.add_argument('--endpoint_prefix', required=True,
            help='your iot endpoint prefix.')
parser.add_argument('--client_cert', required=True,
            help='your client cert file.')
parser.add_argument('--client_key', required=True,
            help='your client key file.')

args = parser.parse_args()
endpoint_prefix = args.endpoint_prefix
client_cert = args.client_cert
client_key = args.client_key

device_name = 'device_x509_mqtt'
region = 'cn-north-1'
private_topic = "IoTDemo/"+device_name

base_path = "./"
server_root_ca_file = base_path + "AmazonRootCA1.pem"
client_cert_file = base_path + client_cert
client_key_file = base_path + client_key

endpoint = "%s.ats.iot.cn-north-1.amazonaws.com.cn" % endpoint_prefix
port = 8883

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
            msg = raw_input()
            private_data = msg
            message = {}
            message['message'] = json.dumps({"source":device_name, "data":private_data})
            message['sequence'] = pri_loopCount
            messageJson = json.dumps(message)
            myAWSIoTMQTTClient.publish(private_topic, messageJson, 1)
            pri_loopCount += 1
    except:
        sys.exit()

if __name__ == '__main__':
    # Init AWSIoTMQTTClient
    myAWSIoTMQTTClient = None
    myAWSIoTMQTTClient = AWSIoTMQTTClient(device_name)
    myAWSIoTMQTTClient.configureEndpoint(endpoint, port)
    myAWSIoTMQTTClient.configureCredentials(server_root_ca_file, client_key_file, client_cert_file)

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
