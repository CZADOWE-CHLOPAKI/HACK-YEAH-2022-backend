import os.path

from app import settings


def create_static_file_uri(path: str):
    if path is None:
        return None
    return f"{settings.HOST}/documents/{os.path.basename(path)}"
