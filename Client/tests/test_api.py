import json
import unittest
from unittest.mock import MagicMock, patch, Mock
import grpc
from client.app import app
from client.helpers.grpc_helper import get_grpc_channel


class TestFactorialAPI(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.client = app.test_client()
        self.headers = {"Authorization": "Bearer valid_token", "Content-Type": "application/json"}

        self.mock_request = Mock()
        self.mock_logger = Mock()

        self.app_context = app.app_context()
        self.app_context.push()

    def test_calculate_factorial_valid_input(self):
        data = {"number": 5}
        response = self.client.post("/factorial", data=json.dumps(data), headers=self.headers)
        result = json.loads(response.get_data(as_text=True))
        self.assertEqual(200, response.status_code)
        self.assertEqual(str(120), result['result'])

    def test_valid_input_with_MagicMock(self):
        data = {"number": 6}
        expected_result = {"result": "720"}

        stub = MagicMock()
        stub.CalculateFactorial.return_value.result = 720

        with app.test_request_context("/factorial", method="POST", json=data, headers=self.headers):
            with app.app_context():
                app.grpc_stub = stub
                response = self.client.post("/factorial", data=json.dumps(data), headers=self.headers)
                self.assertEqual(200, response.status_code)
                self.assertEqual(expected_result, json.loads(response.data))

    def test_calculate_factorial_invalid_input(self):
        data = {"number": "invalid"}
        response = self.client.post("/factorial", data=json.dumps(data), headers=self.headers)
        self.assertEqual(400, response.status_code)

    def test_calculate_factorial_without_input(self):
        response = self.client.post("/factorial", headers=self.headers)
        self.assertEqual(400, response.status_code)

    def test_invalid_input_with_request_context(self):
        data = {"number": "5"}
        with app.test_request_context("/factorial", method="POST", json=data, headers=self.headers):
            response = self.client.post("/factorial", data=json.dumps(data), headers=self.headers)
            self.assertEqual(400, response.status_code)
            self.assertIn("error", json.loads(response.data))

    def test_calculate_factorial_invalid_token(self):
        headers = {'Authorization': "Bearer invalid_token", "Content-Type": "application/json"}
        data = {"number": 5}
        response = self.client.post("/factorial", data=json.dumps(data), headers=headers)
        self.assertEqual(401, response.status_code)

    def test_calculate_factorial_invalid_content_type(self):
        headers = {'Authorization': "Bearer valid_token", "Content-Type": ""}
        data = {"number": 5}
        response = self.client.post("/factorial", data=json.dumps(data), headers=headers)
        self.assertEqual(415, response.status_code)

    @patch('client.app.grpc.insecure_channel')
    def test_get_grpc_channel_success(self, mock_insecure_channel):
        mock_grpc_channel = Mock()
        mock_insecure_channel.return_value = mock_grpc_channel
        future_mock = Mock()
        future_mock.result.return_value = None
        mock_grpc_channel_ready_future = Mock(return_value=future_mock)
        with patch('client.app.grpc.channel_ready_future', mock_grpc_channel_ready_future):
            grpc_channel, error_response = get_grpc_channel(self.mock_request, self.mock_logger)
        self.assertEqual(grpc_channel, mock_grpc_channel)
        self.assertEqual(error_response, "")

    @patch('client.app.grpc.insecure_channel')
    def test_get_grpc_channel_timeout_error(self, mock_insecure_channel):
        mock_insecure_channel.return_value = Mock()
        mock_grpc_channel_ready_future = Mock(side_effect=grpc.FutureTimeoutError())
        with patch('client.app.grpc.channel_ready_future', mock_grpc_channel_ready_future):
            error_msg, error_response = get_grpc_channel(self.mock_request, self.mock_logger)
        self.assertEqual(500, error_response)
        json_error_msg = json.loads(error_msg.get_data())
        self.assertEqual({'error': 'Timeout error connecting to gRPC server'}, json_error_msg)

    @patch('client.app.grpc.insecure_channel')
    def test_get_grpc_channel_unknown_error(self, mock_insecure_channel):
        mock_insecure_channel.return_value = Mock()
        mock_grpc_channel_ready_future = Mock(side_effect=Exception())
        with patch('client.app.grpc.channel_ready_future', mock_grpc_channel_ready_future):
            error_msg, error_response = get_grpc_channel(self.mock_request, self.mock_logger)
        self.mock_logger.exception.assert_called_once_with(
            f"{self.mock_request.remote_addr} - Unexpected error connecting to gRPC server")
        self.assertEqual(500, error_response)
        json_error_msg = json.loads(error_msg.get_data())
        self.assertEqual({'error': 'Unknown error connecting to gRPC server'}, json_error_msg)

    def tearDown(self):
        # remove Flask app context
        self.app_context.pop()


if __name__ == '__main__':
    unittest.main()
