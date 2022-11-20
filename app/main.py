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
from metadata.ultimate_metadata import get_all

app = FastAPI()

origins = ["*"]

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


@app.get("/report")
def get_report(uris: list[str]):
    pass

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
    for fle in converted_files:
        process_file(fle)
        if fle.converted and not error_occurred(fle.errors, 69) and error_occurred(fle.errors, 1001):
            remove_file_signature(fle)

        shutil.copyfile(fle.file_path, settings.PROCESSED_DOCUMENTS_DIR / os.path.basename(fle.file_path))

    report_filepath = None
    for fle in converted_files:
        try:
            print(fle.file_path)
            receiver, sender, document = get_all(fle.file_path)

            report_txt = f"""
--- RECIEVER ---
name: {receiver.name}
nip: {receiver.nip}
pesel: {receiver.pesel}
adress: {receiver.address}

--- SENDER ---
name: {sender.name}
ePUAP: {sender.ePUAP}
email: {sender.email}
adress: {" ".join(sender.adres)}

--- DOCUMENT --- 
number: {document.number}
unp: {document.unp}
date: {document.date}
signee: {document.signee}
            """
            print('aaaabbbb')
            report_filepath = fle.file_path.replace('pdf', 'txt')
            print('report_filepath')
            print(report_filepath)
            with open(report_filepath, 'w') as f:
                f.writelines(report_txt)

            shutil.copyfile(report_filepath, settings.PROCESSED_DOCUMENTS_DIR / os.path.basename(report_filepath))
        except BaseException:
            print('Report could not be generated')
    # save file to filesystem
    # db_document = save_file(file, db)

    # return info about the file
    json_response = {'data': []}
    for fle in converted_files:
        json_response['data'].append({
            'converted': fle.converted,
            # 'path': file.file_path,
            'size': os.path.getsize(fle.file_path),
            'conversion_error': fle.conversion_error,
            'errors': fle.errors,
            'filename': fle.original_filename,
            'uri': create_static_file_uri(fle.file_path),
            'report_uri': create_static_file_uri(report_filepath),
            'sign_data': fle.sign_data,
            'verified_ts': datetime.now().timestamp(),
            'metadata': 'metadata'
        })

    return json_response
