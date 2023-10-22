# gRPC with Background Processes

A sample gRPC client-server streaming large payload in both directions.

## Setting Up

You need to setup local python environment and install some necessary packages

```sh
pyenv virtualenv 3.8.12 041
pyenv local 041
pip install grpcio grpcio-tools
```

## Anatomy of the Server 

The server code consists of 2 parts

1. Stub code (api_pb2*.py). These code files are generated from proto file with following.

```sh
python -m grpc_tools.protoc --proto_path=. ./api.proto --python_out=./server/ --grpc_python_out=./server/
```

2. Custom server code (run.py). This code file imports the stub and spawns the gRPC server.


## Run

To start the server, we run the custom server code.

```sh
python server/run.py
```


## Licence

BSD