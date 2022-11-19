from app import settings


def create_static_file_uri(filename):
    return f"{settings.FIXED_DOCUMENTS_DIR}/{filename}"
