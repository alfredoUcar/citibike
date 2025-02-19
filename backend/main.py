import requests
from fastapi import APIRouter, FastAPI, HTTPException, Depends
from fastapi.responses import StreamingResponse
from models.dataset_request import DatasetRequest

app = FastAPI()
router = APIRouter()


@router.get("/")
def read_root():
    return {"message": "Citibike dataset API"}


@router.get("/dataset/")
def download_data(params: DatasetRequest = Depends()):
    """Downloads the dataset according to the specified year and month."""

    year, month = params.year, params.month

    filename = f"{year}-{month}-dataset.zip" if month else f"{year}-dataset.zip"

    # download file
    file_url = "https://s3.amazonaws.com/tripdata/2013-citibike-tripdata.zip"

    response = requests.get(file_url, stream=True)
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="Dataset not found.")

    def iter_file():
        """Generate data chunks to avoid using too much memory"""
        for chunk in response.iter_content(chunk_size=8192):  # 8 KB per chunk
            yield chunk

    return StreamingResponse(
        iter_file(),
        media_type="application/zip",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )

app.include_router(router)
