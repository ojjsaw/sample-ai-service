import numpy as np
import datetime
import argparse
import json
import requests
import os
import cv2
import time

def create_request(img):
    signature = "serving_default"
    instances = []
    for i in range(0, img.shape[0], 1):
        instances.append({input_tensor_name: img[i].tolist()})
    data_obj = {"signature_name": signature, "instances": instances}
    data_json = json.dumps(data_obj)
    return data_json

# args for the microservice
parser = argparse.ArgumentParser(description='Sends requests via TFS REST API. Displays performance')
parser.add_argument('--images_dir', required=False, default="test-data", help='default: test-data/baseball directory of test images')
parser.add_argument('--size', required=False, default=224, help='width=height default: 224')
parser.add_argument('--labels_list', required=False, default="labels.txt", help='default labels.txt e.g. id labelstring')
parser.add_argument('--rest_url', required=False, default='http://localhost', help='rest url default: http://test-server')
parser.add_argument('--rest_port', required=False, default=8001, help='rest port default: 8001')
args = vars(parser.parse_args())
print(args)

print("starting client test....")

time.sleep(5)

# read all labels and images
size = args['size']
img_array = np.zeros((0,size,size,3), np.float32)
path_array = []
with open(args['labels_list'], 'r') as f:
    labels_map = [x.split(sep=' ', maxsplit=1)[-1].strip() for x in f]
for filename in os.listdir(args['images_dir']):
    path = os.path.join(args['images_dir'],filename)
    img = cv2.imread(path).astype(np.float32)  # BGR color format, shape HWC
    img = img/127.0 - 1 # normalize the image
    img = cv2.resize(img, (size,size)) # h, w of target model input
    img = img.reshape(1,img.shape[0],img.shape[1],3) # change shape to NHWC
    img_array = np.append(img_array, img, axis=0)
    path_array.append(path)


# Get model metadata with REST API
metadata_result = requests.get("{}:{}/v1/models/{}/versions/1/metadata".format(args['rest_url'], args['rest_port'], 'classifyballs'), verify=False)
metadata_result_dict = json.loads(metadata_result.text)
input_tensor_name = list(metadata_result_dict['metadata']['signature_def']['signatureDef']['serving_default']['inputs'].keys())[0]
outputs_tensor_name = list(metadata_result_dict['metadata']['signature_def']['signatureDef']['serving_default']['outputs'].keys())[0]
print("Input Tensor: " + input_tensor_name)
print("Output Tensor: " + outputs_tensor_name)

# Request predictions with REST API
session = requests.Session()
length = len(img_array)
output_array = []
total_time = 0
for i in range(length):
    data_json = create_request(img_array[i:i+1])

    start_time = datetime.datetime.now()
    response = requests.post("{}:{}/v1/models/{}/versions/1:predict".format(args['rest_url'], args['rest_port'], 'classifyballs'), data=data_json, verify=False)
    response.raise_for_status() # handle any errors
    end_time = datetime.datetime.now()

    elapsed_time = response.elapsed.total_seconds()
    total_time += elapsed_time

    # sort and display labels, probability
    print('\nResponse: {:.2f}ms'.format((elapsed_time * 1000)) + ", " + path_array[i])
    probs = response.json()['predictions'][0]
    top_ind = np.argsort(probs)[-10:][::-1]
    for id in top_ind:
        print("{} - {:.7f}".format(labels_map[id], probs[id]))


print('\nREQUEST > NETWORK > INFERENCE > NETWORK > RESPONSE')
print('----------------------------------------------------')
print('Requests to AI Service: {} images'.format(length))
print('Avg Response: {:.2f}ms'.format((total_time * 1000) / length))
print('{:.1f} fps'.format(1000/((total_time * 1000) / length)))
