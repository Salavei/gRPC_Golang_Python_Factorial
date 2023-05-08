from fastapi.testclient import TestClient
from main.main import app
from unittest.mock import patch

client = TestClient(app)


def test_calculate_factorial():
    data = {"number": 5}
    with patch("utils.utils_client.FactorialClient.calculate_factorial") as mock_calc_factorial:
        mock_calc_factorial.return_value = "120"
        response = client.post("/calculate_factorial", json=data, headers={"Authorization": "Bearer abc123"})
        assert response.status_code == 200
        assert response.json() == {"result": "120"}
        mock_calc_factorial.assert_called_once_with(data["number"])


def test_type_error():
    data = {"number": "some_text"}
    response = client.post("/calculate_factorial", json=data, headers={"Authorization": "Bearer abc123"})
    assert response.status_code == 422


def test_authorization_error():
    data = {"number": 5}
    response = client.post("/calculate_factorial", json=data, headers={"Authorization": "invalidtoken"})
    assert response.status_code == 401


def test_authorization_invalid_methods():
    data = {"number": 5}
    delete_method = client.delete("/calculate_factorial", headers={"Authorization": "Bearer abc123"})
    get_method = client.get("/calculate_factorial", headers={"Authorization": "Bearer abc123"})
    put_method = client.put("/calculate_factorial", json=data, headers={"Authorization": "Bearer abc123"})
    patch_method = client.patch("/calculate_factorial", json=data, headers={"Authorization": "Bearer abc123"})
    assert delete_method.status_code == 405
    assert get_method.status_code == 405
    assert put_method.status_code == 405
    assert patch_method.status_code == 405
