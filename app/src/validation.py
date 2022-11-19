import io

from pyhanko.pdf_utils.reader import PdfFileReader


class ValidationError(Exception):
    pass


def validate_digital_signature(file_content: bytes):
    r = PdfFileReader(io.BytesIO(file_content))
    # sig = r.embedded_signatures[0]
    # status = validate_pdf_signature(sig)
    # print(status.pretty_print_details())

    if not len(r.embedded_signatures):
        raise ValidationError('Dokument nie posiada podpisu elektronicznego')


def validate_filetype(path: str) -> bool:
    # load file
    return True
    # check file type


def is_pdf(file_content: bytes) -> bool:
    pdf_magic_number = b'\x25\x50\x44\x46\x2D'
    return file_content[:5] == pdf_magic_number


def validate_file(file_content: bytes, filename: str):
    # check if file is pdf

    validate_digital_signature(file_content)

    # if len(file.filename) > settings.MAX_FILENAME_LENGTH:
    #     raise ValidationError("Nazwa pliku jest za długa (max 255)")
    #
    # if not re.match(settings.FILENAME_REGEX, file.filename):
    #     raise ValidationError("Nazwa pliku zawiera niedozwolone znaki")

    return True

