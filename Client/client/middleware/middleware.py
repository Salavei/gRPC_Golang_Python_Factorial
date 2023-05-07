from flask import jsonify, request
from functools import wraps


def require_token(logger):
    """
        Decorator function that checks for a valid authorization token before
        allowing access to the endpoint.
    """

    def wrapper(func):
        @wraps(func)
        def decorated(*args, **kwargs):
            token = request.headers.get('Authorization')
            if not token or token != 'Bearer valid_token':
                logger.info(f"{request.remote_addr} - Invalid token")
                return jsonify({'error': 'Invalid token'}), 401
            return func(*args, **kwargs)

        return decorated

    return wrapper
