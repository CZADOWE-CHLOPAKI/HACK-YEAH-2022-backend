from fastapi import Depends, FastAPI, HTTPException, UploadFile
from sqlalchemy.orm import Session
from starlette.staticfiles import StaticFiles

from app import settings
from app.src import crud, models, schemas
from app.src.database import SessionLocal, engine
from app.src.uri_utils import create_static_file_uri
from app.src.utils import validate_filetype, save_file_to_disk, validate_file, ValidationError, save_file
import os

# init app
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

os.makedirs(settings.DOCUMENTS_DIR, exist_ok=True)
app.mount("/documents", StaticFiles(directory=settings.FIXED_DOCUMENTS_DIR, html=False), name="site")

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
def upload_documents(document: UploadFile, db: Session = Depends(get_db)):
    try:
        # validate file extension && size
        # validate_filetype(document)
        validate_file(document)
    except ValidationError as e:
        return {
            'error': e
        }

    # save file to filesystem
    path = save_file(document, db)

    # create entry in the db

    # validate file

    # return info about the file
    return {
        "errors": [
            {
                'name': 'asd',
                'corrected': False,
            }
        ],
        'uri': create_static_file_uri()
    }
