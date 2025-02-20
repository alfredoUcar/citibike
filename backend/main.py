import requests
from fastapi import APIRouter, Depends, FastAPI, HTTPException
from fastapi.responses import StreamingResponse

from models.dataset_request import DatasetRequest
from services.dataset_url import DatasetUrlService

app = FastAPI()
router = APIRouter()

CHUNK_SIZE = 8192  # 8 KB per chunk


@router.get("/")
def read_root():
    return {"message": "Citibike dataset API"}


@router.get("/dataset/")
def download_data(params: DatasetRequest = Depends()):
    """Downloads the dataset according to the specified year and month."""

    try:
        file_url = DatasetUrlService(params.year, params.month).get_url()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    response = requests.get(file_url, stream=True)
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="Dataset not found.")

    def iter_file():
        """Generate data chunks to avoid using too much memory"""
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            yield chunk

    filename = (
        f"{params.year}-{params.month}-dataset.zip"
        if params.month
        else f"{params.year}-dataset.zip"
    )
    return StreamingResponse(
        iter_file(),
        media_type="application/zip",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


app.include_router(router)
