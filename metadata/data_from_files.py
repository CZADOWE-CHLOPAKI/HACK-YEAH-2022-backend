import io
from sender import Sender
from receiver import Receiver
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
import re

folder = "/home/lazarus/Desktop/testi"
key_word_sender = "Kontakt:"
key_word_receiver = "Korespondencję otrzymują"
key_word_UNP = "UNP:"
key_word_email = "e-mail:"
key_word_ePUAP = "ePUAP"
key_word_ul = "ul. "
key_word_al = "al. "

def pdf2txt(inPDFfile, outTXTfile):
    inFile = open(inPDFfile, 'rb')
    resMgr = PDFResourceManager()
    retData = io.StringIO()
    txtConverter = TextConverter(resMgr, retData,laparams=LAParams()) 
    interpreter = PDFPageInterpreter(resMgr, txtConverter)
    for page in PDFPage.get_pages(inFile):
        interpreter.process_page(page)
    txt = retData.getvalue()
    with open(outTXTfile, 'w') as f:
        f.write(txt)

def clean_file(infilename):
    outfilename = infilename + "_clean"
    with open(infilename,"r") as f, open(outfilename,"w") as out:
        for line in f:
            if line.strip():
                out.write(line)     

def file2list(filename):
    with open(filename, 'r') as f:
        return f.readlines()
        
#privided that sender is the first non-empty info in the file
def get_sender_key_from_file(filename, lines):
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
            return sender_key, key_index#TODO

def find_value(line, key):
    index = find_loop(line, key) + len(key)
    word = ""
    line = line[index::].lstrip()
    for i in range(len(line)):
        if (line[i] != " "):
            word += line[i]
        else:
            return word
    return word

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
    return line[i::]
    

def find_loop(seq, subseq):
    n = len(seq)
    m = len(subseq)
    for i in range(n - m + 1):
        found = True
        for j in range(m):
            if seq[i + j] != subseq[j]:
                found = False
                break
        if found:
            return i

def get_sender_from_file(filename, filename_clean, lines):
    sender_key, key_index = get_sender_key_from_file(filename)
    sender_key_lower = [x.lower().strip() for x in sender_key]
    lines_lower = [x.lower().strip() for x in lines]
    lines_lower = lines_lower[key_index + len(sender_key)::]
    index = find_loop(lines_lower, sender_key_lower) + len(sender_key_lower)
    name = lines_lower[index]
    return name

def get_UNP(lines):
    for _, line in enumerate(lines):
        index = line.find(key_word_UNP)
        if index != -1:
            return line[index+len(key_word_UNP)::].strip()

# def get_receiver_from_file(filename, infilename_clean, key_word):
#     with open(filename, 'r') as f:
#         lines = f.readlines()
#         for i, line in enumerate(lines):
#             if line.find(key_word) != -1:
#                 name = lines[i+1].strip()
#                 pesel = lines[i+2].strip()
#                 email =  lines[i+3].strip()
#                 telephone = lines[i+4].strip()
#                 sender = Sender(name, position, email, telephone)
#                 return sender


inPDFfile = "/home/lazarus/Desktop/testi/send_hybrid_gov_01.pdf"
infilename = "/home/lazarus/Desktop/testi/send_hybrid_gov_01.txt"
infilename_clean = "/home/lazarus/Desktop/testi/send_hybrid_gov_01_clean.txt"
#print(get_sender_from_file(infilename, infilename_clean))
#print(get_sender_from_file(infilename,infilename_clean))
#sen = get_sender_from_file(outfilename, key_word_sender)
# print(sen)
#print(get_UNP(outfilename, key_word_UNP))
#pdf2txt(inPDFfile, infilename)
#print(get_sender_from_file(infilename, infilename_clean))

lines = file2list(infilename)
# epuap = get_sender_ePAUP(lines)
adres = get_sender_address(lines)
print(adres)
#no_empty_lines_file(infilename, outfilename)


