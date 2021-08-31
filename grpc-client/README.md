Start the model-server before starting the client.

Setup client locally
```
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Run the client
```
sample-ai-service/grpc-client$ python grpc-client.py
{'images_list': '../imgdata/input_images.txt', 'size': 224, 'labels_list': '../model-serving/converted_savedmodel/labels.txt'}
Input: test-data/unknown/t10.jpg
gRPC response time to ai-service:  5.73 ms
ClassID Probability
------- -----------
unknown  0.9991145
cricketball0.0005056
baseball  0.0002019
tennisball 0.0001366
basketball 0.0000415

-----------------

gRPC microservice to OpenVINO Inference Service
[Mobilenet 224x224 Image Classification]
--------------------------------------------------
Average response time:  8.84 ms
Client microservice can process 113.07 frames per second.
```

Build grpc client microservice
```
docker build -t ojjsaw/grpc-client:latest .
```

```
docker run --rm -it ojjsaw/grpc-client:latest
```

## TF Serving perf. comparison
```
python grpc-tf-client.py

{'images_list': 'input_images.txt', 'size': 224, 'labels_list': 'labels.txt', 'address': '127.0.0.1', 'port': '8500'}
Input: test-data/unknown/t10.jpg
gRPC response time to ai-service:  16.84 ms
ClassID Probability
------- -----------
unknown  0.9991143
cricketball0.0005056
baseball  0.0002019
tennisball 0.0001366
basketball 0.0000415

-----------------

gRPC microservice to Tensorflow Inference Service
[Mobilenet 224x224 Image Classification]
--------------------------------------------------
Average response time:  18.50 ms
Client microservice can process 54.05 frames per second.

```