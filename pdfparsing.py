# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 22:26:22 2022

@author: Мария
"""

from pdfrw import PdfReader
from pdfrw import PdfWriter
import pdfplumber
import csv

path = "2aem2020-43-50.pdf"

with pdfplumber.open(path) as pdf:
   for i in range(len(pdf.pages)):
       page = pdf.pages[i]
       table = page.extract_table()
       print(table)
       print()
       #    text = page.extract_text()
       with open('file.csv', 'w') as f:
            writer = csv.writer(f, delimiter=';')
            if table:
                writer.writerows(table)
    
import fitz # install using: pip install PyMuPDF
# в переменную text записываю текст из  пдф
with fitz.open(path) as doc:
    text = ""
    for page in doc:
        text += page.get_text()
        
osnova = ''
ending = text.find('Acknowledgments\n')
if ending == -1:
    ending = text.find('ACKNOWLEDGMENTS')
    if ending == -1:
        ending = text.rfind('References\n')
        if ending == -1:
            ending = text.rfind('REFERENCES')
caption = text.find('Contents\n')
begin = text.find('Introduction\n')
if caption != -1:
    t = begin
    begin = t + 13 + text[t+13:].find('Introduction\n')
if begin == -1:
    begin = text.find('INTRODUCTION')
osnova = text[begin+13:ending]


email = ''
for dog in range(len(text)):
    if text[dog] == '@':
        mailend1 = dog + text[dog:].find('\n')
        mailend2 = dog + text[dog:].find(' ')
        mailend = min(mailend1, mailend2)
        mailbegin1 = text[:dog].rfind('\n')
        mailbegin2 = text[:dog].rfind(' ')
        mailbegin = max(mailbegin1, mailbegin2)
        email += text[mailbegin:mailend]

#pip install pillow
#извлекаю изображения
import PIL.Image
import io
pdf = fitz.open(path)
counter = 1
for i in range(len(pdf)):
    page = pdf[i]
    images = page.get_images()
    for image in images:
        base_img = pdf.extract_image(image[0])
        image_data = base_img['image']
        img = PIL.Image.open(io.BytesIO(image_data))
        extension = base_img['ext']
        img.save(open(f'image{counter}.{extension}', "wb"))
        counter += 1
