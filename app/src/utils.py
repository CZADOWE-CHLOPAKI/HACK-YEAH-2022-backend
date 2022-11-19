import os
import shutil
import uuid
from pathlib import Path

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app import settings
from app.src import crud
from app.src.schemas import DocumentCreate, Document


class ValidationError(Exception):
    pass


def validate_filetype(path: str) -> bool:
    # load file
    return True
    # check file type


def validate_file(file: UploadFile):
    # if len(file.filename) > settings.MAX_FILENAME_LENGTH:
    #     raise ValidationError("Nazwa pliku jest za długa (max 255)")
    #
    # if not re.match(settings.FILENAME_REGEX, file.filename):
    #     raise ValidationError("Nazwa pliku zawiera niedozwolone znaki")

    return True


def save_file(file: UploadFile, db: Session) -> Document:
    # saves to disk and db
    try:
        path = save_file_to_disk(file)
    except:
        raise

    document = DocumentCreate(path=str(path.resolve()), status=0, report='')
    db_document = crud.create_document(db, document)
    return db_document


def save_file_to_disk(file: UploadFile) -> Path:
    filename = uuid.uuid4().hex + '_' + file.filename
    os.makedirs(settings.DOCUMENTS_DIR, exist_ok=True)

    destination = settings.DOCUMENTS_DIR / filename

    try:
        with destination.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    finally:
        file.file.close()

    return destination
