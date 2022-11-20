import asyncio
import shutil
from datetime import datetime

from fastapi import Depends, FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.models import Response
from sqlalchemy.orm import Session
from starlette.staticfiles import StaticFiles

from app import settings
from app.src import models
from app.src.converters import convert_file, ConversionError
from app.src.database import SessionLocal, engine
import os

from app.src.pdf_fixers import remove_file_signature
from app.src.uri_utils import create_static_file_uri
from app.src.utils import error_occurred
from app.src.validation import process_file

app = FastAPI()

origins = [
    "http://localhost:3000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# init app
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

os.makedirs(settings.DOCUMENTS_DIR, exist_ok=True)
os.makedirs(settings.PROCESSED_DOCUMENTS_DIR, exist_ok=True)
app.mount("/documents", StaticFiles(directory=settings.PROCESSED_DOCUMENTS_DIR, html=False), name="site")

dir_path = os.path.dirname(os.path.realpath(__file__))


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# endpoints

@app.post("/documents")
def upload_documents(file: UploadFile):  # , db: Session = Depends(get_db)
    if file.file.__sizeof__() > 8000000:
        return {
            'error': 'Plik jest za duży'
        }

    file_content = asyncio.run(file.read())
    try:
        converted_files = convert_file(file_content, file.filename)
    except ConversionError as e:
        return {'data': [
            {'errors': [{'corrected': False, 'error': 'Typ pliku nie jest wspierany'}], 'filename': file.filename}]
        }
    except Exception as e:
        return {'data': [
            {'errors': [{'corrected': False, 'error': 'Błąd konwersji pliku na plik pdf'}], 'filename': file.filename}]
        }

    # copy files so they are available for download
    for file in converted_files:
        process_file(file)
        if file.converted and not error_occurred(file.errors, 69) and error_occurred(file.errors, 1001):
            remove_file_signature(file)

        shutil.copyfile(file.file_path, settings.PROCESSED_DOCUMENTS_DIR / os.path.basename(file.file_path))

    # save file to filesystem
    # db_document = save_file(file, db)

    # return info about the file
    json_response = {'data': []}
    for file in converted_files:
        json_response['data'].append({
            'converted': file.converted,
            # 'path': file.file_path,
            'size': os.path.getsize(file.file_path),
            'conversion_error': file.conversion_error,
            'errors': file.errors,
            'filename': file.original_filename,
            'uri': create_static_file_uri(file.file_path),
            'sign_data': file.sign_data,
            'verified_ts': datetime.now().timestamp(),
            'metadata': 'metadata'
        })

    return json_response
