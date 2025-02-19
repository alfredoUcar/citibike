from services.dataset_url import DatasetUrlService


def test_url_without_month():
    year = 2013
    month = None
    url_service = DatasetUrlService(year, month)

    expected_url = "https://s3.amazonaws.com/tripdata/2013-citibike-tripdata.zip"
    assert url_service.get_url() == expected_url
