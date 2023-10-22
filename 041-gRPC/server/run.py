import grpc
from concurrent import futures
import time

# Import from generated stubs
import api_pb2_grpc as pb2_grpc
import api_pb2 as pb2


class ApiService(pb2_grpc.StreamServicer):
    
    def __init__(self, *args, **kwargs):
        pass

    def InitiateStream(self, request, context):
        # Extract the message from request
        message = request.message

        print('... Receiving stream initialization request: ', message)

        result = {
            'uid': None,
            'uri': None,
            'offset': None
        }
        return pb2.StreamTicket(**result)


    def GetStream(self, request, context):
        # Extract the message from request
        message = request.message

        print('... Receiving message: ', message)

        # taotodo
        # - how to generate HTTP error codes
        # - how to spawn background process / io-blocking thread?

        result = {}

        # taotodo: generate streaming response
        return pb2.StreamResponse(**result)
    

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=20))
    pb2_grpc.add_StreamServicer_to_server(ApiService(), server)
    
    print('... Server listening to port 2345')
    server.add_insecure_port('[::]:2345')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    print('Starting server ...')
    serve()