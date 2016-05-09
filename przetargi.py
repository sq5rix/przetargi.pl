import sys
import re
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

srch = ''
if len(sys.argv) >= 2:
    for i in range(1, len(sys.argv)):
        srch += sys.argv[i] + ' '
    srch = srch[:-1]
else:
    srch = input("What do you look for? ")

quest = re.sub('\s', '+', srch)
print(quest)
url = 'http://www.przetargi.egospodarka.pl/search.php?submitted=1&phrase=' + quest

headers = {}
headers['User-Agent'] = \
    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"

req = Request(url, headers=headers)
resp = urlopen(req)
resp_data = resp.read()

soup = BeautifulSoup(resp_data, "lxml")
data = {}
for link in soup.find_all('td'):
    key = link.get('data-th')
    if key in data:
        if 'Daty' in key:
            end_date = link.text.partition('\n\n')[2]
            data[key].append(end_date.partition(' ')[0])
        else:
            data[key].append(link.find('a').text)
    else:
        if 'Daty' in key:
            end_date = link.text.partition('\n\n')[2]
            data[key] = [end_date.partition(' ')[0]]
        else:
            data[key] = [link.find('a').text]

print(data)

