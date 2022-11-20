import os
import tempfile
import subprocess
from dataclasses import dataclass, field
import zipfile


def absolute_file_paths(directory):
    for dirpath,_,filenames in os.walk(directory):
        for f in filenames:
            yield os.path.abspath(os.path.join(dirpath, f))


@dataclass
class ConvertedFile:
    file_path: str | None
    original_filename: str = None
    errors: list = field(default_factory=lambda: [])
    conversion_error: bool = False
    converted: bool = True
    sign_data: dict = field(default_factory=lambda: {})

    def add_error(self, error: str, corrected: bool = False, coordinates: dict = None):
        if coordinates is None:
            coordinates = None
        if error is not None:
            self.errors.append({
                'error': error,
                'corrected': corrected,
                'coordinates': coordinates
            })


class ConversionError(Exception):
    pass


class DetectFiletype:

    @dataclass
    class MagicNumbers:
        # https://sceweb.sce.uhcl.edu/abeysekera/itec3831/labs/FILE%20SIGNATURES%20TABLE.pdf
        # https://en.wikipedia.org/wiki/List_of_file_signatures
        PDF = b'\x25\x50\x44\x46\x2D'
        DOCX = b'\x50\x4B\x03\x04\x14\x00\x06\x00'
        XML = b'\x3C\x3F\x78\x6D\x6C\x20'
        ZIP = b'\x50\x4B\x03\x04'
        PPTX = b''
        ODT = b''

    extensions = {
        MagicNumbers.DOCX: '.docx',
        MagicNumbers.XML: '.xml',
        MagicNumbers.ZIP: '.zip',
        MagicNumbers.PPTX: '.pptx',
        MagicNumbers.ODT: '.odt',
        MagicNumbers.PDF: '.pdf',
    }

    @staticmethod
    def detect(file_content: bytes):
        if file_content[:8] == DetectFiletype.MagicNumbers.DOCX:
            return DetectFiletype.MagicNumbers.DOCX
        # if file_content[:6] == DetectFiletype.MagicNumbers.XML:
        #     return DetectFiletype.MagicNumbers.XML
        if file_content[:4] == DetectFiletype.MagicNumbers.ZIP:
            return DetectFiletype.MagicNumbers.ZIP
        if file_content[:5] == DetectFiletype.MagicNumbers.PDF:
            return DetectFiletype.MagicNumbers.PDF

        return None


def xml_to_pdf(file_content: bytes) -> str | None:
    return None


def zip_to_pdf(file_in: str) -> list[ConvertedFile]:
    pdf_file_list = []
    with tempfile.TemporaryDirectory() as tmp_dir:
        with zipfile.ZipFile(file_in, 'r') as zip_ref:
            zip_ref.extractall(tmp_dir)
            file_paths = list(absolute_file_paths(tmp_dir))
            for file_path in file_paths:
                with open(file_path, 'rb') as f:
                    converted_file = convert_file(f.read(), os.path.basename(file_path))
                    pdf_file_list += converted_file

    return pdf_file_list


def docx_to_pdf(file_in: str) -> ConvertedFile:
    # https://github.com/unoconv/unoconv/issues/49#issuecomment-416317222
    file_out = ""
    try:
        file_out = file_in.replace("docx", "pdf")
        p = subprocess.Popen(f"doc2pdf {file_in} -o {file_out}", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
        stdout, stderr = p.communicate()
        p.wait()
    except BaseException as e:
        pass

    return ConvertedFile(file_out, converted=True, conversion_error=(not os.path.isfile(file_out)))


def convert_file(file_content: bytes, original_filename: str) -> list[ConvertedFile]:
    # detekcja rozszerzenia
    file_type = DetectFiletype.detect(file_content)
    print('file type', file_type)
    if file_type is None:
        raise ConversionError('Typ pliku nie jest wspierany')

    with tempfile.NamedTemporaryFile(suffix=DetectFiletype.extensions[file_type], delete=False) as tmp_in:
        tmp_in.write(file_content)

        if file_type == DetectFiletype.MagicNumbers.PDF:
            print('recieved pdf. no conversion')
            return [ConvertedFile(file_path=tmp_in.name, converted=False, conversion_error=False, original_filename=original_filename)]

        if file_type == DetectFiletype.MagicNumbers.ZIP:
            print("converting zip file")
            return zip_to_pdf(tmp_in.name)

        if file_type == DetectFiletype.MagicNumbers.DOCX:
            print("converting docx file")
            converted = docx_to_pdf(tmp_in.name)
            converted.original_filename = original_filename
            return [converted, ]

    raise ConversionError('Typ pliku nie jest wspierany')