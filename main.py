import requests
from fake_headers import Headers
from bs4 import BeautifulSoup
import re
import time
import json
from alive_progress import alive_bar


def get_headers():

    '''Заголовки для get запросов'''

    return Headers(browser='chrome', os='win').generate()

def get_parametres(num):

    '''Параметры для get запросов'''

    return {
        'text': 'python',
        'area': [1, 2],
        # 'area': 1146,
        'page': num,
        'hhtmFrom': 'vacancy_search_list'
    }

def get_requests(url, params=None, class_=None, **kwargs):
    while True:
        html = requests.get(url, headers=get_headers(), params=params)
        soup = BeautifulSoup(html.text, features="lxml")
        div = soup.find('div', class_=class_, attrs=kwargs)
        if div:
            if params != None:
                serp_items = div.find_all('div', class_="serp-item", 
                                        attrs=[attrs1, attrs2, attrs3])
                return div, soup, serp_items
            else:
                description = soup.find('div', attrs={"class": [
                                                    "vacancy-branded-user-content", 
                                                    "vacancy-description"
                                                    ]}).text
                pattern1 = re.search(r'[Dd]jango', description)
                pattern2 = re.search(r'[Ff]lask', description)
                pattern3 = re.search(r'[Aa][Pp][Ii]', description)
                # print(pattern3)#, pattern2)
                if pattern1 or pattern2 or pattern3:
                    append_list(div)
                return

def append_list(div):
    my_dict['fields']['company'] = i.find('a', 
        attrs={"data-qa": "vacancy-serp__vacancy-employer"}).text
    my_dict['fields']['city'] = i.find('div', class_="bloko-text", 
        attrs={"data-qa": "vacancy-serp__vacancy-address"}).text
    my_dict['fields']['salary'] = div.find('div', 
        attrs={"data-qa": "vacancy-salary"}).text
    my_dict['fields']['tittle'] = i.find('a').text
    my_json.append(my_dict)
    save_json()

def save_json():
    with open('web_parser.json', 'w', encoding='UTF-8') as f:
        json.dump(my_json, f, ensure_ascii=False, indent=2)   


if __name__ == '__main__':
    url = 'https://spb.hh.ru/search/vacancy'

    attrs1 = {"data-qa": "vacancy-serp__vacancy vacancy-serp__vacancy_premium"}
    attrs2 = {"data-qa": "vacancy-serp__vacancy vacancy-serp__vacancy_standard_plus"}
    attrs3 = {"data-qa": "vacancy-serp__vacancy vacancy-serp__vacancy_standard"}

    count = 0
    end_page = True
    my_json = []
    a = time.perf_counter()
    while end_page:
        div, soup, serp_items = get_requests(url, get_parametres(count), id="a11y-main-content")
        end_page = soup.find('a', class_="bloko-button", rel="nofollow", attrs={"data-qa": "pager-next"})
        if not end_page:
            print('Последний лист')
            print('Страница: ', count + 1)
            end_page = False
        else:
            print('Страница: ', count + 1)
            
        with alive_bar(len(serp_items), force_tty=True, dual_line=True) as bar:
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
                bar.text = f'Download {i.find("a").text}, please wait ...'
                get_requests(my_dict['link'], class_="vacancy-title")
                bar()
                
        print('-' * 80)
        count += 1
                
    b = time.perf_counter()
    print('Время работы:', b - a)
            
