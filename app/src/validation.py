import io

from pyhanko.pdf_utils.reader import PdfFileReader
from pyhanko.sign.validation import validate_pdf_signature

from app.src.converters import ConvertedFile


class ValidationError(Exception):
    pass


def validate_digital_signature(file_path: str):
    with open(file_path, 'rb') as f:
        r = PdfFileReader(io.BytesIO(f.read()))

    if not len(r.embedded_signatures):
        return 'Dokument nie posiada podpisu elektronicznego'

    sig = r.embedded_signatures[0]
    status = validate_pdf_signature(sig)

    return {
        'subject': status.signing_cert.subject.human_friendly,
        'trusted': status.trusted,
        'valid': status.valid and status.intact
    }


def validate_filetype(path: str) -> bool:
    # load file
    return True
    # check file type


def is_pdf(file_content: bytes) -> bool:
    pdf_magic_number = b'\x25\x50\x44\x46\x2D'
    return file_content[:5] == pdf_magic_number


def validate_file(file: ConvertedFile):
    # check if file is pdf
    x = validate_digital_signature(file.file_path)
    if type(x) == str:
        file.add_error(x)
    else:
        file.sign_data = x


    # if len(file.filename) > settings.MAX_FILENAME_LENGTH:
    #     raise ValidationError("Nazwa pliku jest za długa (max 255)")
    #
    # if not re.match(settings.FILENAME_REGEX, file.filename):
    #     raise ValidationError("Nazwa pliku zawiera niedozwolone znaki")
