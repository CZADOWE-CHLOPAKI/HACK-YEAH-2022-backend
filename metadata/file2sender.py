from utils import *
from classes import *

key_word_email = "e-mail:"
key_word_ePUAP = "ePUAP"
key_word_ul = "ul. "
key_word_al = "al. "

#privided that sender is the first non-empty info in the file
def get_sender_title(txt_file):
    lines = file2list(txt_file)
    key_index = 0
    for i in range(len(lines)):
        if lines[i].strip():
            key_index = i
            break
    sender_key = []
    for i in range(key_index, len(lines), 1):
        if lines[i].strip():
            sender_key.append(lines[i].strip())
        else:
            return sender_key, key_index
    return sender_key, key_index

def get_sender_email(lines):
    index = 0
    for i in range(len(lines)):
        if lines[i].find(key_word_email) != -1:
            index = i
            break
    line = lines[index]
    email = re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', line)
    return email.group(0)

def get_sender_ePAUP(lines):
    index = 0
    for i in range(len(lines)):
        if lines[i].find(key_word_email) != -1:
            index = i
            break
    line = lines[index]
    return find_value(line, key_word_ePUAP)

def get_sender_address(lines):
    index = 0
    key = ""
    for i in range(len(lines)):
        if lines[i].find(key_word_ul) != -1:
            index = i
            key = key_word_ul
            break
        elif lines[i].find(key_word_al) != -1:
            index = i
            key = key_word_al
            break
    line = lines[index]
    i = find_loop(line, key)
    return line[i::].rstrip()

def file2receiver(pdf_path):
    txt_file = pdf2txt(pdf_path)
    txt_file_clean = clean_file(txt_file)
    lines = file2list(txt_file_clean)
    name, _ = get_sender_title(txt_file)
    name = " ".join(name)
    address = get_sender_address(lines)
    email = get_sender_email(lines)
    ePUAP = get_sender_ePAUP(lines)
    sender = Sender(name, address, email, ePUAP)
    print(sender)
    return sender

path = folder + "/" + file
# file2receiver(path)
