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
Input: /home/ojjsaw/ovms-test/sample-ai-service/imgdata/test/basketball/unnamed.jpg
ClassID Probability
------- -----------
basketball  0.9533881
tennisball 0.0432762
cricketball0.0016672
unknown  0.0008490
baseball  0.0008195
--------------------------------
gRPC client request-response time to ai-service:  9.18 ms
```

Build grpc client microservice
```
docker build -t ojjsaw/grpc-client:latest .
```

```
docker run --rm -it ojjsaw/grpc-client:latest /bin/bash
```