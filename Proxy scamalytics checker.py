import time
from time import sleep
import requests
from itertools import cycle
from timeit import default_timer
from lxml import html
import pprint
import sys

proxy_amount = int(input("Please enter amount of proxies to be checked: "))

userInput = sys.stdin.readlines()
proxy = list(map(str.strip, userInput))

pp = pprint.PrettyPrinter(indent=2)

tally = {">15":0,
         "100":0,
         "Duplicates":0}

proxlist = []
iplist = {}

proxy_pool = cycle(proxy)
print("Starting\n")
start = default_timer()

for i in range(proxy_amount):
    con = bool(True)
    session = requests.Session()
    next_proxy = next(proxy_pool)
    
    try:
        ip = session.get("http://icanhazip.com", proxies={"http": next_proxy}, timeout=2).text

    #Goes onto next proxy if the current one times out
    except requests.exceptions.Timeout or ReadTimeout or RemoteDisconnected:
        continue

    #Checks for duplicates and skips them if found
    for m in proxlist:
        if ip == m:
            con = bool(False)

    if con == bool(False):
        tally["Duplicates"] = tally.get("Duplicates") + 1
        continue
    
    proxlist.append(ip)
    iplist[i]=next_proxy, ip


n = -1
for x in proxlist:
    n += 1
    url = "https://www.scamalytics.com/ip/" + x
    page = requests.get(url)
    #Pauses the code to let the page load, adjust for slower internet connections
    time.sleep(0.3)
    tree = html.fromstring(page.content)
    score = tree.xpath('//div[@class="score" and text()]/text()')

    try:
        mod_score = int(str(score).strip("[']").split()[2])
    except ValueError:
        pass

    #Removes any results that are higher than 15
    if mod_score > 15:
        tally[">15"] = tally.get(">15") + 1
        if mod_score == 100:
            tally["100"] = tally.get("100") + 1
        try:
            iplist.pop(n)
        except KeyError:
            pass
        continue

    #Adds the fraud score to the proxy
    try:
        iplist[n] += tuple(score)
    except KeyError:
        pass

pp.pprint(iplist)
print("\n")
for x in tally:
    print(x,": ",tally[x])
print("\nTime: ", str(round((default_timer() - start), 3)))
