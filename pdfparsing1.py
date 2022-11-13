# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 22:26:22 2022

@author: Мария
"""

from pdfrw import PdfReader
from pdfrw import PdfWriter
import pdfplumber
import csv

path = "D:/university/2course/project/2201.00648.pdf"
    
import fitz # install using: pip install PyMuPDF
# в переменную text записываю текст из  пдф
with fitz.open(path) as doc:
    text = ""
    for page in doc:
        text += page.get_text()
        
osnova = ''

text.rfind('References\n')
ending = text.rfind('Acknowledgments\n')
if ending == -1:
    ending = text.rfind('ACKNOWLEDGMENTS')
    if ending == -1:
        ending = text.rfind('References\n')
        if ending == -1:
            ending = text.rfind('REFERENCES')
caption = text.find('Contents\n')
begin = text.rfind('Introduction\n')
'''
if caption != -1:
    t = begin
    begin = t + 13 + text[t+13:].find('Introduction\n')'''
if begin == -1:
    begin = text.find('INTRODUCTION')

ending
osnova = text[begin+13:ending]
osnova


#чистка текста
import re

def remove_text_between_parens(text):
    n = 1  # run at least once
    while n:
        text, n = re.subn(r'\([^()]*\)', '', text)  # remove non-nested/flat balanced parts
        text, n  = re.subn(r'\[[^\]]+\]', '', text)
    return text 

osnova = remove_text_between_parens(osnova)
osnova
#удаоление номеров страниц
#osnova = re.sub(r'\n\d+\n', '', osnova)

reg = re.compile('[^a-zA-Z0-9%\- \. \n]')
osnova = reg.sub('', osnova)
osnova = osnova.replace('  ', '')
osnova = osnova.replace('-\n', '')
osnova1 = osnova.split('\n')
osnova1
#удаление сносок
i = 0
while i < len(osnova1):
    #print(i)
    if any(c.isupper() for c in osnova1[i][:osnova1[i].find(' ')]) and osnova1[i][:osnova1[i].find(' ')][0].isdigit() and osnova1[i].count(' ') >= 1:
        j = i + 1
        while not osnova1[j].isdigit():
            j += 1
        #print(osnova1[j])
        #print('lala')
        print(osnova1[i:j+1])
        print('kuku')
        print(i, j)
        #osnova1.remove(osnova1[i:j+1])
        del osnova1[i:j+1]
        i -= 1
    i += 1
osnova1
#удаление строк без букв, с не более 2 словами и при этом без точек, строки только с log
i = 0  
while i < len(osnova1):
    if not any(c.isalpha() for c in osnova1[i]) or osnova1[i] == ' log 'or (osnova1[i].count(' ') <= 1 and osnova1[i].find('.') == -1) or (osnova1[i].count(' ') <= 1 and osnova1[i].find('.') == -1):
        print(osnova1[i])
        print('kuku')
        osnova1.remove(osnova1[i])
        i -= 1
    else:
        #удаление слов, в середине которых есть буквы
        osnova1[i] = re.sub(r'\w+\d+\w+', '', osnova1[i])
        #удаление строк, в которых максимальная лдина слова - 4
        if max([len(x) for x in osnova1[i].split(' ')]) <= 4:
            #print(osnova1[i])
            osnova1.remove(osnova1[i])
            i -= 1
    i += 1
osnova1

i = 0

osnova = ' '.join(osnova1)
osnova = osnova.replace('\n', ' ')
osnova

#for delete digits after words without strips
for i in osnova.split(' '):
    if any(c.isalpha() for c in i) and any(c.isdigit() for c in i):
        i = re.sub(r'\d+$', '', i)
        print(i)

osnova
osnova = " ".join(osnova.split())
osnova = osnova.replace(' .', '.')

print(osnova)

############

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
