from fastapi import Depends, FastAPI, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.src import crud, models, schemas
from app.src.database import SessionLocal, engine
from app.src.utils import validate_filetype, save_file_to_disk, validate_file, ValidationError, save_file

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


import os
dir_path = os.path.dirname(os.path.realpath(__file__))

print(dir_path)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items



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
    save_file(document, db)

    # create entry in the db

    # validate file

    # return info about the file
    return {'filename': document.filename}
    # return {"filenames": [file.filename for file in files]}
