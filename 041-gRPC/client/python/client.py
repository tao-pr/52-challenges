import grpc
from pprint import pprint

# Import from generated stubs
import api_pb2_grpc as pb2_grpc
import api_pb2 as pb2


if __name__ == '__main__':
    # Prepare client from stub
    channel = grpc.insecure_channel('localhost:2345')
    stub = pb2_grpc.StreamStub(channel)

    # Call method #1 - initiate stream
    status = stub.InitiateStream(pb2.Package(uid='123', uri='test-file'))
    print(f'InitiateStream: returns {status}')

    # Call method #2 - get stream
    offsets = [0, 1, 2, 4, 10, 24, 25, 100]
    for offset in offsets:
        response = stub.GetStream(pb2.StreamTicket(
            uid='123', uri='test-file', offset=offset))
        if response.isEOF:
            print(f'Get chunk #{offset} -> FAILED/EOF')
        else:
            print(
                f'Get chunk #{offset} -> {len(response.body) / 1024} KB ... {response.body[:3]}')
