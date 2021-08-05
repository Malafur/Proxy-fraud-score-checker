import time
from time import sleep
import requests
from itertools import cycle
from lxml import html
import pprint
import sys

proxy_amount = int(input("Please enter amount of proxies to be checked: "))

userInput = sys.stdin.readlines()
proxy = list(map(str.strip, userInput))

pp = pprint.PrettyPrinter(indent=2)

proxlist = []
iplist = {}

proxy_pool = cycle(proxy)


for i in range(proxy_amount):
    session = requests.Session()
    next_proxy = next(proxy_pool)
    
    try:
        ip = session.get("http://icanhazip.com", proxies={"http": next_proxy}, timeout=2).text

    #Goes onto next proxy if the current one times out
    except requests.exceptions.Timeout or ReadTimeout or RemoteDisconnected:
        continue
    
    proxlist.append(ip)
    iplist[i]=next_proxy, ip

n = -1
for x in proxlist:
    n += 1
    url = "https://www.scamalytics.com/ip/" + x
    page = requests.get(url)
    #Pauses the code to let the page load, adjust for slower internet connections
    time.sleep(0.2)
    tree = html.fromstring(page.content)
    score = tree.xpath('//div[@class="score"]/text()')

    #Adds the fraud score to the proxy
    try:
        iplist[n] += tuple(score)
    except KeyError:
        pass

pp.pprint(iplist)
