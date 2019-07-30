#!/usr/bin/env python
# -*- coding: utf-8 -*-

import boto3
import argparse
import json

#获取参数
parser = argparse.ArgumentParser(description='Send data to IoT Core')
parser.add_argument('--data', default="data from device_IAM_http",
            help='data to IoT core topic')
parser.add_argument('--AccessKeyId', required=True,
            help='AccessKeyId')
parser.add_argument('--SecretAccessKey', required=True,
            help='SecretAccessKey')

args = parser.parse_args()
data = args.data
access_key_id = args.AccessKeyId
secret_access_key = args.SecretAccessKey

device_name = 'device_IAM_http'
region = 'cn-north-1'
topic = "IoTDemo/"+device_name

iot_data_client = boto3.client('iot-data',region_name=region,aws_access_key_id=access_key_id,aws_secret_access_key=secret_access_key)

response = iot_data_client.publish(
    topic=topic,
    qos=0,
    payload=json.dumps({"source":device_name, "data":data})
)
print response
