## To test locally
```
python3 -m venv venv
source venv/bin/activate
pip install opencv-python-headless requests
```

## Build the docker image
```
docker build -f restclient.Dockerfile -t ojjsaw/rest-client:latest .
```

## Run the docker image
```
docker run --rm -it ojjsaw/rest-client:latest --rest_url http://localhost
```