FROM python:3.8-slim-buster

WORKDIR /app

# copy python client and data
COPY requirements.txt .
COPY grpc-client.py .
COPY input_images.txt .
COPY labels.txt .
COPY test-data /app/test-data

# install client requirements
RUN pip3 install --no-cache-dir -r requirements.txt
RUN rm -rf /var/lib/apt/lists/*

CMD ["/app/grpc-client.py"]
ENTRYPOINT [ "python3" ]

