FROM openvino/model_server:latest

# Copy model container, ensure files have 777
COPY ./ov_model/ /models/classifyballs

# Copy model-server-config into model-server container
COPY model-server-config.json /model-server-config.json

ENTRYPOINT [ "/bin/bash", "-c", "/ovms/bin/ovms --port 9001 --rest_port 8001 --config_path /model-server-config.json --log_level INFO" ]