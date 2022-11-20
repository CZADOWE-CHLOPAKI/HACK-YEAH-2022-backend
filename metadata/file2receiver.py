from utils import *
from classes import *

key_word_PESEL = "PESEL:"
key_word_NIP = "NIP:"

def get_receiver_name_and_address(lines):
    index = 0
    for i, line in enumerate(lines):
        postal_code = re.search(r'(\d{2}(\-\d{3}) )', line)
        if(postal_code != None):
            index = i
            break
    name = lines[index-2].strip()
    address = lines[index-1].rstrip() + lines[index].rstrip()
    return name, address

def get_receiver_pesel_or_nip(lines):
    index = 0
    key = ""
    for i in range(len(lines)):
        if lines[i].find(key_word_PESEL) != -1:
            index = i
            key = key_word_PESEL
            break
        elif lines[i].find(key_word_NIP) != -1:
            index = i
            key = key_word_NIP
            break
    line = lines[index]
    return find_value(line, key), key 

def file2receiver(pdf_path):
    txt_file = pdf2txt(pdf_path)
    txt_file_clean = clean_file(txt_file)
    lines = file2list(txt_file_clean)
    name, address = get_receiver_name_and_address(lines)
    pesel_or_nip, key = get_receiver_pesel_or_nip(lines)
    if key==key_word_PESEL:
        new_pesel = pesel_or_nip
        receiver = Receiver(name, address, new_pesel, nip=None)
        print(receiver)
        return receiver
    elif key==key_word_NIP:
        new_nip = pesel_or_nip
        receiver = Receiver(name, address, pesel=None, nip=new_nip)
        print(receiver)
        return receiver

path = folder + "/" + file
# file2receiver(path)
