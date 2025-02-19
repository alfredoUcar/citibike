import requests
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse

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

    filename = f"{year}-{month}-dataset.zip" if month else f"{year}-dataset.zip"

    # download file
    file_url = "https://s3.amazonaws.com/tripdata/2013-citibike-tripdata.zip"

    response = requests.get(file_url, stream=True)
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="Dataset not found.")

    def iter_file():
        """Genera chunks de datos para enviar al cliente sin consumir demasiada memoria"""
        for chunk in response.iter_content(chunk_size=8192):  # 8 KB por chunk
            yield chunk

    return StreamingResponse(
        iter_file(),
        media_type="application/zip",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )
