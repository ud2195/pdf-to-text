# -*- coding: utf-8 -*-
"""
Created on Tue May 28 11:15:46 2019

@author: udayk
"""

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import io
from PIL import Image
import pytesseract
from wand.image import Image as wi

def convert(fname, pages=None,encoding='utf-8'):
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    infile = open(fname, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    if len(text)>=500:
        print('pdfminer')
        with open(r'D:\New folder\textfile1.txt', 'a+',encoding="utf-8") as f:
            f.write(text)
            return text
    else:
        print('OCR')
        pdffile = wi(filename = fname, resolution = 300)
        pdfImg = pdffile.convert('jpeg')

        imgBlobs = []

        for img in pdfImg.sequence:
            page = wi(image = img)
            imgBlobs.append(page.make_blob('jpeg'))


        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        extracted_text = []
        for imgBlob in imgBlobs:
            im= Image.open(io.BytesIO(imgBlob))
            text2 = pytesseract.image_to_string(im, lang = 'eng')
        with open(r'D:\New folder\textfile2.txt', 'a+',encoding="utf-8") as z:
            z.write(text2)
            return text2



