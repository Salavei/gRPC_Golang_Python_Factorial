from flask import jsonify


def is_valid_input(data):
    """
    This function checks if the input data contains a key called 'number'
    and if its value is an integer. If the data is valid, the function returns True. Otherwise, it returns False.

    Parameters:
    data: A dictionary containing the input data.

    Returns:
    True if the input data is valid, otherwise False.
    """
    if 'number' not in data or not isinstance(data['number'], int):
        return False
    return True


def is_valid_type(request):
    """
    This function checks if the content type of the incoming request is 'application/json'
    and if the input data is valid according to the is_valid_input function. If the content
    type or input data is invalid, the function returns a JSON-encoded error response with
    a 415 or 400 status code, respectively.

    Parameters:
    request: A Flask request object representing the incoming HTTP request.

    Returns:
    If the request is valid, returns None.
    If the content type of the request is unsupported, returns a JSON-encoded error response with a 415 status code.
    If the input data is invalid, returns a JSON-encoded error response with a 400 status code.
    """
    content_type = request.headers.get('Content-Type')
    if content_type != 'application/json':
        return jsonify({'error': 'Unsupported Content-Type. Please use application/json.'}), 415
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({'error': 'Invalid input. Please provide an integer number.'}), 400
    if not is_valid_input(data):
        return jsonify({'error': 'Invalid input. Please provide an integer number.'}), 400
