import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def get_invalid_dates():
    return [
        ("2012"),
        ("2012/12"),
        ("2025/02"),
        ("2026"),
    ]


@pytest.mark.parametrize("invalid_date", get_invalid_dates())
@pytest.mark.skip(reason="moved to model")
def test_returns_error_if_date_out_of_range(invalid_date):
    response = client.get("/dataset/" + invalid_date)
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Invalid year. Supported range: 2013 - 2025-01."
    }
