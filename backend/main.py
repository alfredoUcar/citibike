from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/download/{year}/{month}")
@app.get("/download/{year}")
def download_data(year: int, month: int = None):
    """Downloads the dataset according to the specified year and month."""

    if year < 2013 or (year == 2025 and month != 1) or year > 2025:
        raise HTTPException(
            status_code=400, detail="Invalid year. Supported range: 2013 - 2025-01."
        )

    # TODO: Implement the download logic here, this is just a placeholder
    return {"year": year, "month": month}
