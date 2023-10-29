import grpc
from grpc_reflection.v1alpha import reflection
from concurrent import futures
import time
from task import background
import asyncio

# Import from generated stubs
import api_pb2_grpc as pb2_grpc
import api_pb2 as pb2


class ApiService(pb2_grpc.StreamServicer):

    def __init__(self, *args, **kwargs):
        pass

    def InitiateStream(self, request, context):
        # Extract the message from request

        print('... Receiving stream initialization request: ', request)

        status = asyncio.run(background.check_progress(
            request.uid, request.uri, offset=0))
        if status == background.Status.PENDING:
            # Still pending, returns idempotent offset
            result = {
                'uid': request.uid,
                'uri': request.uri,
                'status': 'pending'
            }
            return pb2.StreamTicket(**result)

        elif status == background.Status.READY:
            # Still pending, returns idempotent offset
            result = {
                'uid': request.id,
                'uri': request.uri,
                'status': 'ready'
            }
            return pb2.StreamTicket(**result)

        elif status == background.Status.UNAUTH:
            # Unauthorised
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details('Unauthorised request')
            return pb2.StreamTicket()

        elif status == background.Status.UNKNOWN_URI:
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details('Unknown URI')
            return pb2.StreamTicket()

    def GetStream(self, request, context):
        # Extract the message from request

        print('[API] Receiving message: ', request)

        chunk = asyncio.run(background.get_chunk(
            request.uid, request.uri, request.offset))

        if not isinstance(chunk, background.Status):
            # valid
            result = {
                'uri': request.uri,
                'offset': request.offset,
                'isEOF': False,
                'body': chunk
            }
            return pb2.StreamResponse(**result)
        else:
            # invalid, returns as EOF
            result = {
                'uri': request.uri,
                'offset': request.offset,
                'isEOF': True,
                'body': chunk
            }
            return pb2.StreamResponse(**result)


async def serve():
    # Compression at server level https://github.com/grpc/grpc/tree/master/examples/python/compression#server-side-compression
    server = grpc.server(
        thread_pool=futures.ThreadPoolExecutor(max_workers=20),
        compression=grpc.Compression.Gzip)
    pb2_grpc.add_StreamServicer_to_server(ApiService(), server)

    # Add server reflection
    service_ref = (
        pb2.DESCRIPTOR.services_by_name['Stream'].full_name,
        reflection.SERVICE_NAME
    )
    reflection.enable_server_reflection(service_ref, server)

    print('... Server listening to port 2345')
    server.add_insecure_port('[::]:2345')  # without TLS
    server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    print('Starting server ...')
    asyncio.run(serve())
