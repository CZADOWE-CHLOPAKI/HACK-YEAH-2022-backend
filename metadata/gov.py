import os
from PyPDF2 import PdfFileReader

def file_extention(path):
    _, extension = os.path.splitext(path)
    return extension[1::]

def extention_is_valid(path_ext, valid_exts):
    return path_ext in valid_exts

def file_is_signed():
    pass

def check_if_vertical_and_A4(pdf_path):
    pdf_reader = PdfFileReader(pdf_path)
    for i in range(pdf_reader.numPages):
        page_width = pdf_reader.getPage(i).cropBox.getWidth()
        page_height = pdf_reader.getPage(i).cropBox.getHeight()
        if (not (595.31 < page_width < 595.33 and 841.91 < page_height < 841.93)):
            return False
    return True

def check_standard(pdf_path):
    pass