from PyPDF2 import PdfReader, PdfWriter, PdfFileWriter

from PyPDF2 import PdfFileReader

from app.src.converters import ConvertedFile


def remove_empty_pages(file_in: ConvertedFile):
    pdf_writer = PdfFileWriter()
    pdf_reader = PdfFileReader(file_in.file_path)
    no_pages = pdf_reader.getNumPages()

    page_sizes = []
    for page in range(no_pages):
        page_content = pdf_reader.getPage(page).extract_text()
        page_sizes.append(len(page_content))

    pages_to_add = [i for i, size in enumerate(page_sizes) if size > 200]

    if len(page_sizes) != len(pages_to_add):
        for page in pages_to_add:
            pdf_writer.addPage(pdf_reader.getPage(page))

        with open(file_in.file_path, 'wb') as fh:
            pdf_writer.write(fh)

        file_in.add_error("Z pliku pdf zostały usunięte puste strony", corrected=True)


def remove_file_signature(file_in: ConvertedFile):
    pdf_writer = PdfFileWriter()
    pdf_reader = PdfFileReader(file_in.file_path)

    for page in pdf_reader.pages:
        pdf_writer.addPage(page)

    with open(file_in.file_path, 'wb') as fh:
        pdf_writer.write(fh)

    file_in.add_error("Z pliku pdf został usunięty podpis cyfrowy", corrected=True)