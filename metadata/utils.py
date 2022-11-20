from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
import os
import io
import re


folder = "/home/lazarus/Desktop/testi"
file = "send_hybrid_gov_01.pdf"

def pdf2txt(inPDFfile):
    outTXTfile = os.path.splitext(inPDFfile)[0]+'.txt'
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
    return outTXTfile

def clean_file(infilename):
    outfilename = os.path.splitext(infilename)[0] + "_clean" + ".txt"
    with open(infilename,"r") as f, open(outfilename,"w") as out:
        for line in f:
            if line.strip():
                out.write(line) 
    return outfilename

def file2list(filename):
    with open(filename, 'r') as f:
        return f.readlines()

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