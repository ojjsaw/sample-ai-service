# sample-ai-service
Workflow for cloud-native applications with AI-driven intelligence.

- Leverage transfer learning on teachable-machine **(current)**, lobe.ai, azure custom vision cognitive services, aws sagemaker, etc.
- Import model from above tools and convert to OpenVINO IR 
- OpenVINO Model Server (AI Service) for deploying on cloud or locally on-prem edge device.
- Measure metrics for grpc client microservice for external loadbalancing in the cloud or connecting with other services belonging to an application.

<img src="tm2.PNG" alt="Teachable Machine 2 Training" width="400">

```
sample-ai-service$ docker-compose up
.
.
.
.
.
client-service_1  | -----------------
client-service_1  |
client-service_1  | Input: test-data/tennisball/t8.png
client-service_1  | gRPC response time to ai-service:  23.72 ms
client-service_1  | ClassID Probability
client-service_1  | ------- -----------
client-service_1  | tennisball 0.5555996
client-service_1  | unknown  0.1912299
client-service_1  | basketball 0.1756625
client-service_1  | cricketball0.0465893
client-service_1  | baseball   0.0309187
client-service_1  |
client-service_1  | -----------------
client-service_1  |
client-service_1  | Input: test-data/unknown/t10.jpg
client-service_1  | gRPC response time to ai-service:  18.17 ms
client-service_1  | ClassID Probability
client-service_1  | ------- -----------
client-service_1  | unknown  0.9991145
client-service_1  | cricketball0.0005056
client-service_1  | baseball  0.0002019
client-service_1  | tennisball 0.0001366
client-service_1  | basketball 0.0000415
client-service_1  |
client-service_1  | -----------------
client-service_1  |
client-service_1  | gRPC microservice to OpenVINO Inference Service
client-service_1  | [Mobilenet 224x224 Image Classification]
client-service_1  | --------------------------------------------------
client-service_1  | Average response time:  34.21 ms
client-service_1  | Client microservice can process 29.24 frames per second.

```