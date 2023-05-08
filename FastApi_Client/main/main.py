import os

from fastapi import FastAPI, Depends
from typing import Dict

from middleware.token_authenticate import authenticate
from utils.utils_client import FactorialClient

app = FastAPI()

client = FactorialClient(os.getenv("GO_SERVER_HOST"), os.getenv("GO_SERVER_PORT"))


@app.post("/calculate_factorial")
async def calculate_factorial(data: Dict[str, int], token: str = Depends(authenticate)):
    """
    Calculates the factorial of a number.

    Args:
        data (Dict[str, int]): A dictionary containing the number to calculate the factorial for.
        token (str): Authentication token.

    Returns:
        Dict[str, str]: A dictionary containing the result of the calculation.
    """
    number = data.get('number')
    result = await client.calculate_factorial(number)
    return {"result": result}
