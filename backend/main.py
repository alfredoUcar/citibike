import io
import zipfile

import requests
from fastapi import APIRouter, Depends, FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

from logger import logger
from models.dataset_request import DatasetRequest
from services.dataset_url import DatasetUrlService

app = FastAPI()
router = APIRouter()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # allow frontend requests in dev
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

CHUNK_SIZE = 1024*1024  # 1MB


@router.get("/")
def read_root():
    return {"message": "Citibike dataset API"}


def download_single_file(url: str):
    filename = url.split("/")[-1]
    response = requests.get(url, stream=True)
    logger.debug("Downloading %s", url)
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="Dataset not found.")
    
    # Get file size from Content-Length header if available
    file_size = response.headers.get("Content-Length")

    def iter_file():
        """Generate data chunks to avoid using too much memory"""
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            yield chunk
    
    headers = {
        "Content-Disposition": f"attachment; filename={filename}",
    }

    # Only include Content-Length if we got it from the external server
    if file_size:
        headers["Content-Length"] = file_size

    return StreamingResponse(
        iter_file(),
        media_type="application/zip",
        headers=headers,
    )


def download_multiple_files(file_urls: list[str]):
    memory_zip = io.BytesIO()

    with zipfile.ZipFile(memory_zip, mode="w", compression=zipfile.ZIP_DEFLATED) as zipf:
        for idx, url in enumerate(file_urls):
            logger.debug("Downloading... %s", url)
            response = requests.get(url, stream=True)
            if response.status_code != 200:
                logger.error(
                    "Error downloading dataset from %s. Code: %s, message: %s",
                    url,
                    response.status_code,
                    response.content,
                )
                raise HTTPException(
                    status_code=404, detail=f"Failed to download dataset from {url}"
                )

            file_name = url.split("/")[-1]

            # Write directly to ZIP without loading the whole file into memory
            with zipf.open(file_name, "w") as zip_entry:
                for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                    zip_entry.write(chunk)

    # Finalize ZIP file
    memory_zip.seek(0)
    file_size = memory_zip.getbuffer().nbytes  # Get total ZIP size

    def zip_generator():
        """Stream the ZIP file in chunks"""
        while chunk := memory_zip.read(CHUNK_SIZE):
            yield chunk

    merged_filename = "merged-dataset.zip"
    return StreamingResponse(
        zip_generator(),
        media_type="application/zip",
        headers={
            "Content-Disposition": f"attachment; filename={merged_filename}",
            "Content-Length": str(file_size)  # Include file size for progress tracking
        },
    )


@router.get("/dataset/")
def download_data(params: DatasetRequest = Depends()):
    """Downloads and merges multiple ZIP files into a single ZIP without loading everything into memory."""

    try:
        file_urls = DatasetUrlService(params.year, params.month).get_urls()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    if not file_urls:
        raise HTTPException(status_code=404, detail="No datasets found.")

    logger.debug("urls: %s", file_urls)

    if len(file_urls) == 1:
        return download_single_file(file_urls[0])

    return download_multiple_files(file_urls)


app.include_router(router)
