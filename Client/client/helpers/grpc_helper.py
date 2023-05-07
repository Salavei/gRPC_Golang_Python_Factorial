import grpc
from flask import jsonify
import os

go_server_host = os.getenv("GO_SERVER_HOST", "localhost")
go_server_port = os.getenv("GO_SERVER_PORT", "3000")

def get_grpc_channel(request, logger):
    """
    This function creates an insecure gRPC channel to connect to a gRPC server running on localhost:3000.
    If the connection is successful, the function returns the gRPC channel and an empty string.
    If the connection times out, the function logs an error
    and returns a JSON-encoded error response with a 500 status code.

    Parameters:

    request: A Flask request object representing the incoming HTTP request.
    Returns:

    grpc_channel: An insecure gRPC channel that can be used to communicate with the gRPC server.
    error_response: An empty string if the gRPC connection is successful,
    or a JSON-encoded error response with a 500 status code if the connection times out.
    """
    try:
        grpc_channel = grpc.insecure_channel(f"{go_server_host}:{go_server_port}")
        grpc.channel_ready_future(grpc_channel).result(timeout=10)
        return grpc_channel, ""
    except grpc.FutureTimeoutError:
        logger.exception(f"{request.remote_addr} - Timeout error connecting to gRPC server")
        return jsonify({'error': 'Timeout error connecting to gRPC server'}), 500
    except Exception:
        logger.exception(f"{request.remote_addr} - Unexpected error connecting to gRPC server")
        return jsonify({'error': 'Unknown error connecting to gRPC server'}), 500

