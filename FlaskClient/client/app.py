from flask import Flask, jsonify, request
from logging.handlers import RotatingFileHandler
import logging.handlers
import grpc
from client.helpers.grpc_helper import get_grpc_channel
from client.helpers.input_validator import is_valid_type
from client.middleware.middleware import require_token
from client.services.factorial_service import FactorialService

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

# Create a file log handler
handler = RotatingFileHandler('./logs/app.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)

# Adding a handler to the Flask application logger
app.logger.addHandler(handler)


@app.route('/factorial', methods=['POST'])
@require_token(app.logger)
def calculate_factorial() -> jsonify:
    """
    Calculates factorial for the given number.

    The input should be a JSON object with a single key, `number`, whose
    value is the integer to calculate the factorial for.

    Returns a JSON object with a single key, `result`, whose value is the
    calculated factorial.
    """

    try:

        is_valid = is_valid_type(request)
        if is_valid:
            return is_valid
        data = request.get_json()
        grpc_channel, err = get_grpc_channel(request, app.logger)
        factorial_service = FactorialService(grpc_channel)
        result = factorial_service.calculate_factorial(data['number'])
        app.logger.info(f"{request.remote_addr} - Calculation successful for number: {data['number']}")
        return jsonify({
            'result': result
        })
    except Exception as e:
        app.logger.exception(f"{request.remote_addr} - Unexpected error: {e}")
        return jsonify({'error': 'Unexpected error'}), 500


if __name__ == '__main__':
    app.run()
