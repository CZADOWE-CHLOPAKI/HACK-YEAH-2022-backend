from PyPDF2 import PdfReader
from utils import *

path = folder + "/" + file

from PyPDF2 import PdfReader
import svgwrite

reader = PdfReader(path)
page = reader.pages[2]
dwg = svgwrite.Drawing("GeoBase_test.svg", profile="tiny")

def visitor_svg_rect(op, args, cm, tm):
    if op == b"re":
        (x, y, w, h) = (args[i].as_numeric() for i in range(4))
        dwg.add(dwg.rect((x, y), (w, h), stroke="red", fill_opacity=0.05))

page.extract_text(
    visitor_operand_before=visitor_svg_rect
)
dwg.save()