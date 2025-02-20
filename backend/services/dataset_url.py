class DatasetUrlService:
    def __init__(self, year: int, month: int = None):
        self.year = year
        self.month = month

    def get_urls(self) -> list:
        """Construct the URL for the dataset based on the year and month."""
        base_url = "https://s3.amazonaws.com/tripdata"

        if self.year == 2025:
            if self.month is not None and self.month > 1:
                raise ValueError("Only january is available for year 2025")
            filename = "202501-citibike-tripdata.zip"
            return [f"{base_url}/{filename}"]

        if self.month is None:
            if self.year < 2024:
                filename = f"{self.year}-citibike-tripdata.zip"
                return [f"{base_url}/{filename}"]
            else:  # 2024
                return [
                    f"{base_url}/{self.year}{month:02d}-citibike-tripdata.csv.zip" 
                    if month <= 4 
                    else f"{base_url}/{self.year}{month:02d}-citibike-tripdata.zip"
                    for month in range(1, 13)
                ]

        # month provided
        formatted_month = "{:02d}".format(self.month)
        if self.year > 2023:
            if self.month <= 4:
                filename = f"{self.year}{formatted_month}-citibike-tripdata.csv.zip"
            else:
                filename = f"{self.year}{formatted_month}-citibike-tripdata.zip"
            return [f"{base_url}/{filename}"]

        if (
            self.year > 2015 or self.year == 2015 and self.month >= 9
        ):  # after 2015-09 inclusive
            filename = f"JC-{self.year}{formatted_month}-citibike-tripdata.csv.zip"
            return [f"{base_url}/{filename}"]

        if self.year < 2015 or self.year == 2015 and self.month < 9:  # before 2015-09
            filename = f"{self.year}-citibike-tripdata.zip"
            return [f"{base_url}/{filename}"]

        return []
