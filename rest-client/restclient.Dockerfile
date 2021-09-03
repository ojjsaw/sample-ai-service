FROM python:3.8-slim

WORKDIR /app

# install client requirements
RUN pip install --no-cache-dir opencv-python-headless requests

# copy python client and data
COPY rest-client.py .
COPY labels.txt .
COPY test-data /app/test-data

ENTRYPOINT [ "python", "/app/rest-client.py"]