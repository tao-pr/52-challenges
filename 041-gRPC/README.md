# gRPC with Background Processes

A sample gRPC client-server streaming large payload in both directions.

## Setting Up

You need to setup local python environment and install some necessary packages

```sh
pyenv virtualenv 3.8.12 041
pyenv local 041
pip install grpcio grpcio-tools grpcio-reflection
```

(Optional) install grpc-cli toolset [instruction here](https://github.com/grpc/grpc/blob/master/doc/command_line_tool.md)

## Anatomy of the Server 

The server code consists of 2 parts

1. Stub code (api_pb2*.py). These code files are generated from proto file with following.

```sh
python -m grpc_tools.protoc --proto_path=. ./api.proto --python_out=./server/ --grpc_python_out=./server/
```

2. Custom server code (run.py). This code file imports the stub and spawns the gRPC server.


## Start the server

Before starting the server, start redis by running:

```sh
docker-compose up --no-recreate
```

To start the server, we run the custom server code.

```sh
python server/run.py
```

## Generate sample stream file

Run this script to generate a binary file at *./data/test-file*

```sh
python server/gen_data_file.py
```

## Test with (grp)curl

Get grpcurl from https://github.com/fullstorydev/grpcurl

```sh
# Run -plaintext to disable TLS
# This will list the reflection of service methods

grpcurl -plaintext localhost:2345 list

#grpc.reflection.v1alpha.ServerReflection
#unary.Stream

grpcurl -plaintext localhost:2345 list unary.Stream

#unary.Stream.GetStream
#unary.Stream.InitiateStream
```

Test service invocation

```sh
# Test unauthorised request
grpcurl -plaintext -d '{"uid":"unauth", "uri":"test-file"}' localhost:2345 unary.Stream.InitiateStream

# Test legit request (need to generate data file beforehand)
grpcurl -plaintext -d '{"uid":"111", "uri":"test-file"}' localhost:2345 unary.Stream.InitiateStream

# Test legic request
grpcurl -plaintext -d '{"uid":"111", "uri":"test-file", "offset": 1}' localhost:2345 unary.Stream.GetStream
```

## Run the client

```sh
python client/python/client.py
```

## Stop dependencies

You can stop the dependency by

```sh
docker-compose down
```

## Additional Resources

- [HTTP 1.1 vs HTTP 2](https://www.cloudflare.com/en-gb/learning/performance/http2-vs-http1.1/)
- [gRPC Python basics](https://grpc.io/docs/languages/python/basics/)
- [gRPC error model](https://grpc.io/docs/guides/error/)
- [gRPC async stream python sample](https://github.com/grpc/grpc/blob/master/examples/python/async_streaming/server.py)
- [Asyncio task](https://docs.python.org/3/library/asyncio-task.html)
- [gRPCurl](https://github.com/fullstorydev/grpcurl)


## Licence

BSD