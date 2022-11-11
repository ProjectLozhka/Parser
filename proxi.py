import random
import os
from time import sleep
from lxml.html import fromstring
import requests
from itertools import cycle
import traceback


def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr')[:10]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    return proxies


# If you are copying and pasting proxy ips, put in the list below proxies = ['121.129.127.209:80',
# '124.41.215.238:45169', '185.93.3.123:8080', '194.182.64.67:3128', '106.0.38.174:8080', '163.172.175.210:3128',
# '13.92.196.150:8080']
def proxies_array():
    proxies = get_proxies()
    proxy_pool = cycle(proxies)
    url = 'https://httpbin.org/ip'
    res = []
    for i in range(1, 11):
        # Get a proxy from the pool
        proxy = next(proxy_pool)
        print("Request #%d" % i)
        try:
            response = requests.get(url, proxies={"http": proxy, "https": proxy})
            print(response.json())
            res.append(proxy)
        except:
            # Most free proxies will often get connection errors. You will have retry the entire request using another
            # proxy to work. We will just skip retries as it's beyond the scope of this tutorial, and we are only
            # downloading a single url
            print("Skipping. Connnection error")
    return res


# print(proxies_array())
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
#response = requests.get('http://httpbin.org/ip', proxies=proxies)
#print(response.text)

# list of VPN server codes
codeList = ["TR", "US-C", "US", "US-W", "CA", "CA-W",
            "FR", "DE", "NL", "NO", "RO", "CH", "GB", "HK"]

try:

    # connect to VPN
    os.system("windscribe connect")
    while True:
        # assigning a random VPN server code
        choiceCode = random.choice(codeList)

        # changing IP after a particular time period
        sleep(random.randrange(120, 300))

        # connecting to a different VPN server
        print("!!! Changing the IP Address........")
        os.system("windscribe connect " + choiceCode)

except:

    # disconnect VPN
    os.system("windscribe disconnect")
    print("sorry, some error has occurred..!!")