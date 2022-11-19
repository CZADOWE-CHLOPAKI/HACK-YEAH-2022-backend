from pathlib import Path

from app import settings


def create_static_file_uri(path: Path):
    return f"{settings.HOST}/documents/{path.name}"
