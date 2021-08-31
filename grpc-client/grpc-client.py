import cv2, datetime, grpc
import numpy as np
from tensorflow import make_tensor_proto, make_ndarray
from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2_grpc
import argparse

# args for the microservice
parser = argparse.ArgumentParser(description='Sends requests via TFS gRPC API. Displays performance')
parser.add_argument('--images_list', required=False, default="input_images.txt", help='default: input_images.txt file of labeled images e.g. images/x.jpg 104')
parser.add_argument('--size', required=False, default=224, help='width=height default: 224')
parser.add_argument('--labels_list', required=False, default="labels.txt", help='default labels.txt e.g. id labelstring')
parser.add_argument('--address', required=False, default='127.0.0.1', help='grpc ip address default: 127.0.0.1')
parser.add_argument('--port', required=False, default=9001, help='grpc port default: 9001')
args = vars(parser.parse_args())
print(args)

# read input image list
with open(args['images_list']) as f:
    lines = f.readlines()

# read all images and labels
size = args['size']
img_array = np.zeros((0,size,size,3), np.float32)
label_array = np.zeros((0,1), np.int64)
path_array = []
for line in lines:
    path, label = line.strip().split(" ")
    img = cv2.imread(path).astype(np.float32)  # BGR color format, shape HWC
    img = img/127.0 - 1 # normalize the image
    img = cv2.resize(img, (size,size)) # h, w of target model input
    img = img.reshape(1,img.shape[0],img.shape[1],3) # change shape to NHWC
    img_array = np.append(img_array, img, axis=0)
    label_array = np.append(label_array, int(label))
    path_array.append(path)

# grpc initialization
address = "{}:{}".format(args['address'],args['port'])
channel = grpc.insecure_channel(address)
stub = prediction_service_pb2_grpc.PredictionServiceStub(channel)
request = predict_pb2.PredictRequest()
request.model_spec.name = "classifyballs"

frame_counter = 0
start_time = 0
end_time = 0

img = img_array[0:1]
request.inputs["sequential_1_input"].CopyFrom(make_tensor_proto(img, shape=(img.shape)))

start_time = datetime.datetime.now()
result = stub.Predict(request, 10.0) # result includes a dictionary with all model outputs
end_time = datetime.datetime.now()

output = make_ndarray(result.outputs["StatefulPartitionedCall/sequential_4/sequential_3/dense_Dense2/Softmax"])

with open(args['labels_list'], 'r') as f:
    labels_map = [x.split(sep=' ', maxsplit=1)[-1].strip() for x in f]

print("\nInput: " + path_array[0])
classid_str = "ClassID"
probability_str = "Probability"
for i, probs in enumerate(output):
    probs = np.squeeze(probs)
    top_ind = np.argsort(probs)[-10:][::-1]
    print(classid_str, probability_str)
    print("{} {}".format('-' * len(classid_str), '-' * len(probability_str)))
    for id in top_ind:
        det_label = labels_map[id] if labels_map else "{}".format(id)
        label_length = len(det_label)
        space_num_before = (len(classid_str) - label_length) // 2
        space_num_after = len(classid_str) - (space_num_before + label_length) + 2
        space_num_before_prob = (len(probability_str) - len(str(probs[id]))) // 2
        print("{}{}{}{}{:.7f}".format(' ' * space_num_before, det_label,
                                          ' ' * space_num_after, ' ' * space_num_before_prob,
                                          probs[id]))

duration =  '{:.2f} ms'.format((end_time - start_time).total_seconds()*1000)       
print("--------------------------------")
print("gRPC client request-response time to ai-service: ", duration)






