import io

import PyPDF2
from PyPDF2 import PdfReader
from PyPDF2.errors import FileNotDecryptedError
from pyhanko.pdf_utils.reader import PdfFileReader
from pyhanko.sign.validation import validate_pdf_signature

from app.src.converters import ConvertedFile
from app.src.pdf_fixers import remove_empty_pages


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


def process_file(file: ConvertedFile):
    try:
        reader = PdfReader(file.file_path)
        # don't delete, here be dragons
        # (header.pages generator needs to yield at least once)
        print(reader.pages[0])
    except FileNotDecryptedError:
        file.add_error('Plik nie może być zaszyfrowany', corrected=False, error_code=1001)
        return

    file_good = remove_empty_pages(file)
    if not file_good:
        return

    # common validation
    if len(reader.get_form_text_fields().keys()) > 0:
        file.add_error('Plik nie może zawierać form', corrected=False)

    x = validate_digital_signature(file.file_path)
    if type(x) == str:
        file.add_error(x, error_code=69)
    else:
        file.sign_data = x

