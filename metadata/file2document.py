from utils import *
from classes import *
from file2sender import get_sender_title

key_word_UNP = "UNP:"
key_word_number = "Znak sprawy:"

def get_document_UNP(lines):
    for _ , line in enumerate(lines):
        index = line.find(key_word_UNP)
        if index != -1:
            return line[index+len(key_word_UNP)::].strip()

def get_document_signee(txt_file):
    clean_f = clean_file(txt_file)
    clean_lines = file2list(clean_f)
    sender_title, key_index = get_sender_title(txt_file)
    sender_key_lower = [x.lower().strip() for x in sender_title]
    lines_lower = [x.lower().strip() for x in clean_lines]
    lines_lower = lines_lower[key_index + len(sender_title)::]
    index = find_loop(lines_lower, sender_key_lower) + len(sender_key_lower)
    name = lines_lower[index]
    return name.strip()

def get_document_number(lines):
    for _ , line in enumerate(lines):
        index = line.find(key_word_number)
        if index != -1:
            return line[index+len(key_word_number)::].strip()

def get_document_date(lines):
    for line in lines:
        date = re.search(r'([0-9]?[0-9]+ [a-zA-Z]+ [0-9]{4} )', line)
        if (date != None):
            return date.group(0)

def file2document(pdf_path):
    txt_file = pdf2txt(pdf_path)
    lines = file2list(txt_file)
    unp = get_document_UNP(lines)
    signee = get_document_signee(txt_file)
    number = get_document_number(lines)
    date = get_document_date(lines)
    document = Document(number, unp, date, signee)
    print(document)
    return document

path = folder + "/" + file
file2document(path)