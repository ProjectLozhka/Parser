import lxml
import requests
from bs4 import BeautifulSoup
import re
import csv
from fake_useragent import UserAgent
import random
import time


def pars_title(url):
    proxies, hdr = proxies_headers()
    response = requests.get(url, headers=hdr, proxies=proxies)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = ''
    quotes = soup.find_all('h1', class_='title mathjax')
    for quote in quotes:
        title += quote.text

    annotation = ''
    quotes = soup.find_all('blockquote', class_='abstract mathjax')
    for quote in quotes:
        annotation += quote.text

    pdf = 'https://export.arxiv.org'
    quotes = soup.find_all('a', class_='abs-button download-pdf')
    for quote in quotes:
        pdf += quote['href']
    res = [title, annotation, pdf]
    return res


def pars_for_month_in_year(url, writer):
    proxies, hdr = proxies_headers()
    n = 1
    response = requests.get(url, proxies=proxies, headers=hdr)
    soup = BeautifulSoup(response.text, 'html.parser')
    quotes = soup.find_all('a', title='Abstract')
    base_url = 'https://export.arxiv.org'
    for quote in quotes:
        try:
            row = pars_title(base_url + quote['href'])
            print('Wrote row: ' + str(n))
            writer.writerow(row)
            n += 1
        except:
            print('Error1')
    pass


def take_url_for_all(url):
    proxies, hdr = proxies_headers()
    response = requests.get(url, proxies=proxies, headers=hdr)
    base_url = 'https://export.arxiv.org'
    soup = BeautifulSoup(response.text, 'html.parser')
    quotes = soup.find_all('small')
    n = len(quotes)
    quote = quotes[n - 3].find_all('a')
    n = len(quote)
    res = base_url + quote[n - 1]['href']
    return res


def pars_for_months(url):
    proxies, hdr = proxies_headers()
    response = requests.get(url, headers=hdr, proxies=proxies)
    base_url = 'https://export.arxiv.org'
    soup = BeautifulSoup(response.text, 'html.parser')
    quotes = soup.find('ul')
    quotes = quotes.find_all('li')
    res = []
    for quote in quotes:
        quote_1 = quote.find('a')
        res.append(base_url + quote_1['href'])
    return res


def pars_for_years(url):
    proxies, hdr = proxies_headers()
    response = requests.get(url, proxies=proxies, headers=hdr)
    base_url = 'https://export.arxiv.org'
    soup = BeautifulSoup(response.text, 'html.parser')
    quotes = soup.find('ul')
    quotes = quotes.find_all('li')
    res = []
    quotes = quotes[7].find_all('a')
    for quote in quotes:
        res.append(base_url + quote['href'])
    return res


def main_parse_category_bez_sveniy(url, filename):
    f = open(filename, 'w')
    writer = csv.writer(f)
    years = []
    flag_2 = False
    while not flag_2:
        years = pars_for_years(url)
        flag_2 = True
    random.shuffle(years)
    for year in years:
        print('Parsing year: ' + year)
        flag_1 = False
        while not flag_1:
            try:
                months = pars_for_months(year)
                random.shuffle(months)
                flag_1 = True
                for month in months:
                    flag = False
                    while not flag:
                        try:
                            print('Parsing month: ' + month)
                            month = take_url_for_all(month)
                            month = [month]
                            writer.writerow(month)
                            flag = True
                        except:
                            print('Error in month')
                            time.sleep(20)
            except:
                print('Error in year')
                time.sleep(20)
    f.close()
    pass

def proxies_headers():
    ua = UserAgent()
    hdr = {'User-Agent': ua.random,
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}
    proxi = ['185.40.76.9:25739',
             '95.181.163.15:25739',
             '62.76.142.8:25739',
             '46.8.158.186:25739',
             '194.147.114.3:25739',
             '31.184.240.129:25739',
             '46.161.41.148:25739',
             '45.8.125.193:25739',
             '93.189.47.89:25739',
             '93.189.40.69:25739',
             ]
    proxy2 = 'http://uKZtU5TLAVBj:dan-kos1@' + random.choice(proxi)
    proxies = {'http': proxy2}
    return proxies, hdr

main_parse_category_bez_sveniy('https://export.arxiv.org/archive/astro-ph', 'astrophysics4.csv')
# print(pars_for_years('https://arxiv.org/archive/astro-ph'))
# print(pars_for_months('https://arxiv.org/year/astro-ph/22'))
# print(take_url_for_all('https://arxiv.org/list/astro-ph/2201'))
# print(pars_for_month_in_year('https://arxiv.org/list/astro-ph/2201?show=1291'))
# print(pars_title('https://arxiv.org/abs/2201.00021'))