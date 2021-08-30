Setup OpenVINO for model conversion
```
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install openvino-dev[tensorflow2]
```

Convert model to OpenVINO IR
```
mo --saved_model_dir ./converted_savedmodel/model.savedmodel/ --output_dir ./ov_model/1 --input_shape=[1,224,224,3]
chmod -R 777 ov_model
```

[Optional] For local openvino testing with sample application.
```
python teachable_img_openvino_classify.py ./ov_model/1/saved_model.xml ./ov_model/1/saved_model.bin ./converted_savedmodel/labels.txt '../imgdata/test/tennisball/unnamed.png'
```

Build the ai-service
```
docker build -t ojjsaw/classifyserver:latest .

REPOSITORY                       TAG                    IMAGE ID       CREATED              SIZE
ojjsaw/classifyserver            latest                 e822eaa5f54b   28 seconds ago       464MB
```

Run the ai-service
```
docker run --rm -it -p 9001:9001 -p 8001:8001 ojjsaw/classifyserver:latest .
```

Verify models available in the ai-service.
```json
curl http://127.0.0.1:8001/v1/models/classifyballs/versions/1/metadata

{
 "modelSpec": {
  "name": "classifyballs",
  "signatureName": "",
  "version": "1"
 },
 "metadata": {
  "signature_def": {
   "@type": "type.googleapis.com/tensorflow.serving.SignatureDefMap",
   "signatureDef": {
    "serving_default": {
     "inputs": {
      "sequential_1_input": {
       "dtype": "DT_FLOAT",
       "tensorShape": {
        "dim": [
         {
          "size": "1",
          "name": ""
         },
         {
          "size": "224",
          "name": ""
         },
         {
          "size": "224",
          "name": ""
         },
         {
          "size": "3",
          "name": ""
         }
        ],
        "unknownRank": false
       },
       "name": "sequential_1_input"
      }
     },
     "outputs": {
      "StatefulPartitionedCall/sequential_4/sequential_3/dense_Dense2/Softmax": {
       "dtype": "DT_FLOAT",
       "tensorShape": {
        "dim": [
         {
          "size": "1",
          "name": ""
         },
         {
          "size": "5",
          "name": ""
         }
        ],
        "unknownRank": false
       },
       "name": "StatefulPartitionedCall/sequential_4/sequential_3/dense_Dense2/Softmax"
      }
     },
     "methodName": ""
    }
   }
  }
 }
}
```