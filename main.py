import requests
from fake_headers import Headers
from bs4 import BeautifulSoup
import re
import time
import json


def get_headers():
    return Headers(browser='chrome', os='win').generate()

def get_parametres(num):
    return {
        'text': 'python',
        'area': [1, 2],
        'page': num,
        'hhtmFrom': 'vacancy_search_list'
    }

url = 'https://spb.hh.ru/search/vacancy'

attrs1 = {"data-qa": "vacancy-serp__vacancy vacancy-serp__vacancy_premium"}
attrs2 = {"data-qa": "vacancy-serp__vacancy vacancy-serp__vacancy_standard_plus"}
attrs3 = {"data-qa": "vacancy-serp__vacancy vacancy-serp__vacancy_standard"}

a = time.perf_counter()
count = 0
count_py = 1
end_page = True
my_json = []

while end_page:
    while True:
        html = requests.get(url, headers=get_headers(), params=get_parametres(count))
        soup = BeautifulSoup(html.text, features="lxml")
        div = soup.find('div', id="a11y-main-content")
        if div:
            serp_items = div.find_all('div', class_="serp-item", attrs=[attrs1, attrs2, attrs3])
            break
    end_page = soup.find('a', class_="bloko-button", rel="nofollow", attrs={"data-qa": "pager-next"})
    if not end_page:
        print('Последний лист')
        print('Страница: ', count)
        end_page = False
    else:
        print('Будет еще страница')
        print('Страница: ', count)
        
    for i in serp_items:
        my_dict = {
            'link': None,
            'fields': {
                'tittle': None,
                'salary': None,
                'company': None,
                'city': None
                }
            }
        my_dict['link'] = i.find('a').get('href')
        while True:
            new_div = requests.get(my_dict['link'], headers=get_headers()).text
            soup = BeautifulSoup(new_div, features="lxml")
            div = soup.find('div', class_="vacancy-title")
            if div:
                description = soup.find('div', attrs={"class": ["vacancy-branded-user-content", "vacancy-description"]}).text
                pattern1 = re.search(r'[Dd]jango', description)
                pattern2 = re.search(r'[Ff]lask', description)
                print(pattern1, pattern2)
                if pattern1 or pattern2:
                    my_dict['fields']['company'] = i.find('a', attrs={"data-qa": "vacancy-serp__vacancy-employer"}).text
                    my_dict['fields']['city'] = i.find('div', class_="bloko-text", attrs={"data-qa": "vacancy-serp__vacancy-address"}).text
                    my_dict['fields']['salary'] = div.find('div', attrs={"data-qa": "vacancy-salary"}).text
                    my_dict['fields']['tittle'] = i.find('a').text
                    my_json.append(my_dict)
                break 
        print('Объявление: ', count_py)
        print(my_dict['link'])
        print('*' * 40)
        count_py += 1
    print('-' * 80)
    count += 1

with open('web_parser.json', 'w', encoding='UTF-8') as f:
    json.dump(my_json, f, ensure_ascii=False, indent=2)
            
b = time.perf_counter()
print('Время работы:', b - a)
            
