import pytest

from services.dataset_url import DatasetUrlService


@pytest.mark.parametrize("year", range(2013, 2024))
def test_url_for_year_less_than_2024_without_month_use_YYYY_files(year):
    month = None
    url_service = DatasetUrlService(year, month)
    expected_url = f"https://s3.amazonaws.com/tripdata/{year}-citibike-tripdata.zip"
    assert url_service.get_urls()[0] == expected_url


def test_only_january_is_available_in_2025():
    url_service = DatasetUrlService(2025, None)
    expected_url = "https://s3.amazonaws.com/tripdata/202501-citibike-tripdata.zip"
    assert url_service.get_urls()[0] == expected_url

    url_service = DatasetUrlService(2025, 1)
    expected_url = "https://s3.amazonaws.com/tripdata/202501-citibike-tripdata.zip"
    assert url_service.get_urls()[0] == expected_url

    url_service = DatasetUrlService(2025, 2)
    with pytest.raises(ValueError):
        url_service.get_urls()[0]


def test_url_ignores_month_if_date_is_before_2015_09():
    year = 2015
    month = 8
    url_service = DatasetUrlService(year, month)
    expected_url = f"https://s3.amazonaws.com/tripdata/{year}-citibike-tripdata.zip"
    assert url_service.get_urls()[0] == expected_url


@pytest.mark.parametrize("month", range(1, 12))
def test_2024_with_month_uses_YYYYMM_files(month):
    formatted_month = "{:02d}".format(month)  # MM format
    url_service = DatasetUrlService(2024, month)
    expected_url = f"https://s3.amazonaws.com/tripdata/2024{formatted_month}-citibike-tripdata.csv.zip"
    assert url_service.get_urls()[0] == expected_url


@pytest.mark.parametrize(
    "year, month",
    [
        (2015, 9),
        (2016, 5),
        (2017, 9),
        (2018, 12),
        (2019, 6),
        (2020, 3),
        (2021, 11),
        (2022, 7),
        (2023, 12),
    ],
)
def test_uses_JC_YYYYMM_files_when_month_provided_and_year_between_2015_09_and_2023(
    year, month
):
    formatted_month = "{:02d}".format(month)  # MM format
    url_service = DatasetUrlService(year, month)
    expected_url = f"https://s3.amazonaws.com/tripdata/JC-{year}{formatted_month}-citibike-tripdata.zip"
    assert url_service.get_urls()[0] == expected_url


def test_2024_without_month_uses_all_months_files():
    urls = DatasetUrlService(2024).get_urls()
    assert len(urls) == 12
    for month in range(1, 12):
        formatted_month = "{:02d}".format(month)  # MM format
        assert (
            urls[month - 1]
            == f"https://s3.amazonaws.com/tripdata/2024{formatted_month}-citibike-tripdata.csv.zip"
        )
