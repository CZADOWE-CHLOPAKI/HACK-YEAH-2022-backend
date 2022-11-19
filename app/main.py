from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from starlette.staticfiles import StaticFiles

from app import settings
from app.src import models
from app.src.database import SessionLocal, engine
from app.src.uri_utils import create_static_file_uri
from app.src.utils import validate_file, ValidationError, save_file
import os


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
models.Base.metadata.create_all(bind=engine)

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
def upload_documents(file: UploadFile, db: Session = Depends(get_db)):
    try:
        # validate file extension && size
        # validate_filetype(document)
        validate_file(file)
    except ValidationError as e:
        return {
            'error': e
        }

    # save file to filesystem
    db_document = save_file(file, db)

    # create entry in the db

    # validate file

    # "errors": [
    #     {
    #         'name': 'asd',
    #         'corrected': False,
    #     }
    # ],
    # 'uri': create_static_file_uri()

    # return info about the file
    return {
        'uri': create_static_file_uri(Path(db_document.path))
    }
