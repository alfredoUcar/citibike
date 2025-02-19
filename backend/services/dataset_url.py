class DatasetUrlService:
    def __init__(self, year: int, month: int = None):
        self.year = year
        self.month = month

    def get_url(self) -> str:
        """Construct the URL for the dataset based on the year and month."""
        base_url = "https://s3.amazonaws.com/tripdata"

        filename = "2013-citibike-tripdata.zip"  ## TODO: calculate dataset

        return f"{base_url}/{filename}"
