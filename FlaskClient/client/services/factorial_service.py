from client.factorial import factorial_pb2_grpc, factorial_pb2


class FactorialService:
    """
    This class represents a gRPC client for the Factorial service.
    It provides a method for calculating the factorial of a given number using the Factorial service.

    Methods:
    init(self, grpc_channel): Constructor that initializes the FactorialStub using the specified gRPC channel.
    calculate_factorial(self, number): Method that sends a gRPC request to the
    Factorial service to calculate the factorial of the given number.

    Parameters:
    grpc_channel: A gRPC channel used to connect to the Factorial service.
    number: An integer representing the number whose factorial should be calculated.

    Returns:
    The calculated factorial of the input number.
    """

    def __init__(self, grpc_channel):
        self.stub = factorial_pb2_grpc.FactorialStub(grpc_channel)

    def calculate_factorial(self, number):
        """
        This function sends a gRPC request to the Factorial service to calculate the factorial of the given number.

        Parameters:
        number: An integer representing the number whose factorial should be calculated.

        Returns:
        The calculated factorial of the input number.
        """
        factorial_request = factorial_pb2.FactorialRequest(number=number)
        factorial_response = self.stub.CalculateFactorial(factorial_request)
        return factorial_response.result
