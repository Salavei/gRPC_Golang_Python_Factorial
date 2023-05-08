import grpc
from utils.utils_pb2 import FactorialRequest
from utils.utils_pb2_grpc import FactorialStub


class FactorialClient:
    def __init__(self, host: str, port: str) -> None:
        """
        Initializes a client to communicate with the gRPC service.

        Args:
            host (str): Hostname of the gRPC service.
            port (str): Port number of the gRPC service.
        """
        self.host = host
        self.port = port
        self.channel = grpc.aio.insecure_channel(f"{host}:{port}")
        self.stub = FactorialStub(self.channel)

    async def calculate_factorial(self, number: int) -> str:
        """
        Calculates the factorial of a given number.

        Args:
            number (int): The number to calculate the factorial for.

        Returns:
            int: The calculated factorial value.
        """
        request = FactorialRequest(number=number)
        response = await self.stub.CalculateFactorial(request)
        return response.result
