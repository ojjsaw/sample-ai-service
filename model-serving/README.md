```
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install openvino-dev[tensorflow2]
```

```
mo --saved_model_dir ./converted_savedmodel/model.savedmodel/ --output_dir ./ov_model/1 --input_shape=[1,224,224,3]
chmod -R 777 ov_model
```

```
python teachable_img_openvino_classify.py ./ov_model/1/saved_model.xml ./ov_model/1/saved_model.bin ./converted_savedmodel/labels.txt '../imgdata/test/tennisball/unnamed.png'
```

```
docker build -t ojjsaw/classifyserver:latest .

REPOSITORY                       TAG                    IMAGE ID       CREATED              SIZE
ojjsaw/classifyserver            latest                 e822eaa5f54b   28 seconds ago       464MB
```

```
docker run --rm -it -p 9001:9001 -p 8001:8001 ojjsaw/classifyserver:latest .
```