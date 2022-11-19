import os
import shutil
import uuid

from fastapi import UploadFile

from app import settings


def validate_filetype(path: str) -> bool:
    # load file
    return True
    # check file type


def save_file_to_disk(file: UploadFile) -> str:
    filename = uuid.uuid4().hex + '_' + file.filename
    os.makedirs(settings.DOCUMENTS_DIR, exist_ok=True)

    destination = settings.DOCUMENTS_DIR / filename

    try:
        with destination.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    finally:
        file.file.close()

    return destination
