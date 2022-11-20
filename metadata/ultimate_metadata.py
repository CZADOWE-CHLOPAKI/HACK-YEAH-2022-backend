from utils import *
from classes import *
from PyPDF2 import PdfReader
from file2sender import get_sender_title
from file2document import get_document_signee, get_document_date
from file2receiver import get_receiver_pesel_or_nip

path = folder + "/" + file

header_data = []
left_up_data = []
receiver_data = []
date_data = []
footer_data = []

keyword_case = "Sprawa:"
keyword_case_num = "Znak sprawy:"
keyword_contact = "Kontakt:"
keyword_ul = "UL"
keyword_al = "AL"
key_word_ePUAP = "ePUAP"
key_word_PESEL = "PESEL:"
key_word_NIP = "NIP:"
key_word_UNP = "UNP:"
key_word_number = "Znak sprawy:"

def get_header(text, cm, tm, fontDict, fontSize):
    x = tm[4]
    y = tm[5]
    if y > 700 and x < 1000:
        header_data.append(text)

def get_left_up(text, cm, tm, fontDict, fontSize):
    x = tm[4]
    y = tm[5]
    if 450 < y < 700 and x < 300:
        left_up_data.append(text)

def get_receiver(text, cm, tm, fontDict, fontSize):
    x = tm[4]
    y = tm[5]
    if 450 < y < 600 and x > 300:
        receiver_data.append(text)

def get_date(text, cm, tm, fontDict, fontSize):
    x = tm[4]
    y = tm[5]
    if 550 < y < 700 and x > 300:
        date_data.append(text)

def get_footer(text, cm, tm, fontDict, fontSize):
    x = tm[4]
    y = tm[5]
    if  30 < y < 60:
        footer_data.append(text)

def get_data(pdf_path):
    reader = PdfReader(pdf_path)
    page = reader.pages[0]
    page.extract_text(visitor_text=get_header)
    page.extract_text(visitor_text=get_left_up)
    page.extract_text(visitor_text=get_receiver)
    page.extract_text(visitor_text=get_date)
    page.extract_text(visitor_text=get_footer)

def remove_spaces(array):
    res = []
    for ele in array:
        if ele!=" " and ele!="  ":
            res.append(ele)
    return res

def get_data_final(pdf_path):
    final  = []
    get_data(pdf_path)
    lists = [header_data, left_up_data, receiver_data, date_data, footer_data]
    for array in lists:
        res = remove_spaces(array)
        final.append(res)
    return final

def get_case_num(final):
    case_num = ""
    i = final[1].index(keyword_case_num) + 1
    while(True):
        if final[1][i] != '\n':
            case_num += final[1][i]
            i+=1
        else:
            return case_num.replace(" ", "")

def get_unp(final):
    case_num = ""
    i = final[1].index(key_word_UNP) + 1
    while(True):
        if final[1][i] != '\n':
            case_num += final[1][i]
            i+=1
        else:
            return case_num.replace(" ", "")

def get_receiver_name(final):
    res = final[2]
    name = []
    if not res[0].strip():
        res = res[1::]
    for ele in res:
        if ele != "\n":
            name.append(ele)
        else:
            return name
    return " ".join(name)

def get_receiver_address(final):
    res = final[2]
    ul = 0
    al = 0
    if (keyword_ul in res):
        ul = res.index(keyword_ul)
    if (keyword_al in res):
        al = res.index(keyword_al)
    city = res[-1]
    rest = res[ul+al:-1]
    all = "".join(rest)
    ad = all.split("\n")
    return ad[0], ad[1], city

def get_sender_email(final):
    res = "".join(final[4])
    email = re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', res)
    return email.group(0)

def get_sender_ePUAP(final):
    res = final[4]
    if (key_word_ePUAP in res):
        i = res.index(key_word_ePUAP)
        ePUAP = res[i+1]
        return ePUAP

def get_sender_street(final):
    res = final[4]
    i = 0
    for index, ele in enumerate(res):
        if (keyword_ul.lower() in ele or keyword_al.lower() in ele):
            i = index
    street = ""
    while(True):
        if res[i] != ', ' and res[i] != ',':
            street += res[i]
            i += 1
        else:
            return street

def get_sender_zipcode_and_city(final):
    res = final[4]
    postal_code = re.search(r'(\d{2}(\-\d{3}) )', "".join(res))
    postal_code = postal_code.group(0)
    city = res[-1]
    return postal_code, city

def get_receiver_obj(final, path):
    file_txt = pdf2txt(path)
    lines = file2list(file_txt)
    receiver_name = get_receiver_name(final)
    receiver_address = get_receiver_address(final)
    pesel_or_nip, key = get_receiver_pesel_or_nip(lines)
    new_pesel = None
    new_nip = None
    if key==key_word_PESEL:
        new_pesel = pesel_or_nip
    elif key==key_word_NIP:
        new_nip = pesel_or_nip
    receiver = Receiver(receiver_name, receiver_address, new_pesel, new_nip)
    return receiver

def get_sender_obj(final, path):
    file_txt = pdf2txt(path)
    title = get_sender_title(file_txt)
    sender_email = get_sender_email(final)
    sender_ePUAP = get_sender_ePUAP(final)
    sender_street = get_sender_street(final)
    sender_zipcode, sender_city = get_sender_zipcode_and_city(final)
    sender = Sender(title, [sender_street, sender_zipcode, sender_city], sender_email, sender_ePUAP)
    return sender

def get_document_obj(final, path):
    file_txt = pdf2txt(path)
    lines = file2list(file_txt)
    case_num = get_case_num(final)
    signee = get_document_signee(file_txt)
    unp = get_unp(final)
    date = get_document_date(lines)
    document = Document(case_num, unp, date, signee)
    return document

def get_all(path):
    final = get_data_final(path)
    receiver = get_receiver_obj(final, path)
    sender = get_sender_obj(final, path)
    document = get_document_obj(final, path)
    return receiver, sender, document

get_all(path)




    
    