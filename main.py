import lxml
import requests
from bs4 import BeautifulSoup
import re
import csv
from fake_useragent import UserAgent
import random

def pars_title(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    ua = UserAgent()
    hdr = {'User-Agent': ua.random,
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}
    response = requests.get(url, headers=hdr)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = ''
    quotes = soup.find_all('h1', class_='title mathjax')
    for quote in quotes:
        title += quote.text

    annotation = ''
    quotes = soup.find_all('blockquote', class_='abstract mathjax')
    for quote in quotes:
        annotation = quote.text

    pdf = 'https://arxiv.org'
    quotes = soup.find_all('a', class_='abs-button download-pdf')
    for quote in quotes:
        pdf += quote['href']
    res = [title, annotation, pdf]
    return res

def pars_for_month_in_year(url, writer):
    n = 1
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    quotes = soup.find_all('a', title='Abstract')
    base_url = 'https://arxiv.org'
    for quote in quotes:
        try:
            row = pars_title(base_url+quote['href'])
            print('Wrote row: ' + str(n))
            writer.writerow(row)
            n += 1
        except:
            print('Error')
    pass

def take_url_for_all(url):
    response = requests.get(url)
    base_url = 'https://arxiv.org'
    soup = BeautifulSoup(response.text, 'html.parser')
    quotes = soup.find_all('small')
    n = len(quotes)
    quote = quotes[n-3].find_all('a')
    n = len(quote)
    res = base_url + quote[n-1]['href']
    return res

def pars_for_months(url):
    response = requests.get(url)
    base_url = 'https://arxiv.org'
    soup = BeautifulSoup(response.text, 'html.parser')
    quotes = soup.find('ul')
    quotes = quotes.find_all('li')
    res = []
    for quote in quotes:
        quote_1 = quote.find('a')
        res.append(base_url+quote_1['href'])
    return res

def pars_for_years(url):
    response = requests.get(url)
    base_url = 'https://arxiv.org'
    soup = BeautifulSoup(response.text, 'html.parser')
    quotes = soup.find_all('ul')
    quotes = quotes[1].find_all('li')
    res = []
    quotes = quotes[7].find_all('a')
    for quote in quotes:
        res.append(base_url+quote['href'])
    return res

def main_parse_category_bez_sveniy(url, filename):
    f = open(filename, 'w')
    writer = csv.writer(f)
    header = ['Ttile', 'Annotation', 'PDF']
    writer.writerow(header)
    years = pars_for_years(url)
    for year in years:
        print('Parsing year: ' + year)
        try:
            months = pars_for_months(year)
            for month in months:
                try:
                    print('Parsing month: ' + month)
                    month = take_url_for_all(month)
                    pars_for_month_in_year(month, writer)
                except:
                    print('Error in month')
        except:
            print('Error in year')
    f.close()
    pass

main_parse_category_bez_sveniy('https://arxiv.org/archive/astro-ph', 'astrophysics.csv')
#print(pars_for_years('https://arxiv.org/archive/astro-ph'))
#print(pars_for_months('https://arxiv.org/year/astro-ph/22'))
#print(take_url_for_all('https://arxiv.org/list/astro-ph/2201'))
#print(pars_for_month_in_year('https://arxiv.org/list/astro-ph/2201?show=1291'))
#print(pars_title('https://arxiv.org/abs/2201.00021'))