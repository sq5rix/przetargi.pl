import sys
import re
from bs4 import BeautifulSoup
import requests
from time import sleep


def read_page(soup_one_page):
    for link in soup_one_page.find_all('td'):
        key = link.get('data-th')
        if key in data:
            if 'Daty' in key:
                end_date = link.text.partition('\n\n')[2]
                data[key].append(end_date.partition(' ')[0].strip())
            elif 'Przedmiot' in key:
                data[key].append(link.find('a').get('href'))
            else:
                data[key].append(link.find('a').text.strip())
                print(link.find('a').text.strip())
        else:
            if 'Daty' in key:
                end_date = link.text.partition('\n\n')[2]
                data[key] = [end_date.partition(' ')[0].strip()]
            elif 'Przedmiot' in key:
                data[key] = [link.find('a').get('href')]
            else:
                data[key] = [link.find('a').text.strip()]
                print(link.find('a').text.strip())


def read_next_page(passed_soup):
    # <div class="nexpage2" style="float:right;">&nbsp;
    # <a href="/search/status/1/q/%7C%7C%7Cp%B3yta/sort/relevance_desc/offset/3">następna &raquo;</a>
    # </div>
    link = passed_soup.find_all(attrs={'class': 'nexpage2', 'style': 'float:right;'})
    if 0 == len(link):
        return ''
    else:
        return link[0].find('a').get('href')


def print_data(main_url):
    # Zamawiający
    # Daty: publikacji / zakończenia
    # Przedmiot zamówienia
    # Kategoria
    # Miasto
    for pos in range(0, len(data)-1):
        print('Daty   :' + data['Daty: publikacji / zakończenia'][pos])
        print('Przed  :' + main_url + data['Przedmiot zamówienia'][pos])
        print('Zam    :' + data['Zamawiający'][pos])
        print('Miasto :' + data['Miasto'][pos])
        print('Kat    :' + data['Kategoria'][pos])
        print(' ')


data = {}
search_phrase = ''
if len(sys.argv) >= 2:
    for i in range(1, len(sys.argv)):
        search_phrase += sys.argv[i] + ' '
    search_phrase = search_phrase[:-1]
else:
    search_phrase = input("What do you look for? ")

main_url = 'http://www.przetargi.egospodarka.pl'
url = main_url + '/search.php'

headers = {'User-Agent':
           "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"}
values = {'phrase': search_phrase.encode(encoding='iso-8859-2'),
          'submitted': '1'}

req = requests.get(url, params=values, headers=headers)
resp_data = req.content
soup = BeautifulSoup(resp_data, "lxml")

while True:
    read_page(soup)
    url = read_next_page(soup)
    if url == '':
        break
    else:
        print(main_url+url)
        sleep(1.)
        req = requests.get(main_url+url, headers=headers)
        resp_data = req.content
        soup = BeautifulSoup(resp_data, "lxml")

print_data(main_url)


