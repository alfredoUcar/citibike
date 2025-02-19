import pytest
from pydantic import ValidationError

from models.dataset_request import DatasetRequest


def test_valid_cases():
    assert DatasetRequest(year=2015, month=6)
    assert DatasetRequest(year=2023)
    assert DatasetRequest(year=2025, month=12)


def test_invalid_year():
    with pytest.raises(ValidationError):
        DatasetRequest(year=2012, month=5)
    with pytest.raises(ValidationError):
        DatasetRequest(year=2026, month=5)


def test_invalid_month():
    with pytest.raises(ValidationError):
        DatasetRequest(year=2020, month=0)
    with pytest.raises(ValidationError):
        DatasetRequest(year=2020, month=13)
