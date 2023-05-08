<div align="center">
  <h1>gRPC Golang/Python - Factorial</h1>
  <img src="https://grpc.io/img/logos/grpc-icon-color.png" alt="grpc_logo" "width="400" height="300">
  <p>This is a simple gRPC project that showcases how to implement gRPC with Python and Golang, and how to utilize Redis as a caching layer.</p>
</div>


## Overview

The project consists of three components:

- Python Flask server: serves as a RESTful API that receives a POST request containing a number and sends it to the gRPC server.
- Golang gRPC server: serves as a gRPC server that calculates factorials and caches the results using Redis.
- Redis: used as a caching layer to store previously calculated factorials.

## Tests
We have implemented unit tests for the Flask application and integration tests for the gRPC server written in Golang.

To run the tests for the Flask application, navigate to the Client directory and run the following command:
````
python -m unittest discover -s tests/
````
To run the tests for the gRPC server, navigate to the Server/golang directory and run the following command:
````
go test
````
I have used the unittest framework for testing the Flask application, and the default testing framework for Golang.

## Requirements

- Docker
- Docker Compose

## How to Run

To run the project, simply clone the repository and run:

````
docker-compose build
docker-compose up
````


This command will start three containers: the Flask server, the Golang server, and a Redis instance.

The Flask server listens on port 8000 and serves a RESTful API endpoint that accepts a POST request with a JSON payload containing the number to calculate the factorial for. The Golang server listens on port 50052 and serves a gRPC endpoint that calculates factorials. Redis is used as a caching layer to store previously calculated factorials.


## Usage

To use the project, simply send a POST request to [http://localhost:8000/factorial](http://localhost:8000/factorial) with the following JSON payload:

```markdown
{
"number": 10
}
```

This will calculate the factorial of 10 using the Golang server and Redis as a caching layer, and return the result back to the Flask server, which then responds with the result to the client.

## References

* gRPC
* Flask
* Golang gRPC
* Redis
