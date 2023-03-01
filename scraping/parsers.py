import codecs
import requests
from bs4 import BeautifulSoup as BS
from random import randint

__all__ = ('get_work_ua_vacancies', 'get_hh_vacancies', 'get_avito_vacancies')

headers = [
    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:53.0) Gecko/20100101 Firefox/53.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
    ]
def get_work_ua_vacancies(url, city=None, language=None):
    domain = 'https://www.work.ua'
    res = requests.get(url, headers=headers[randint(0, 2)])
    jobs = []
    errors = []
    if url:
        if res.status_code == 200:
            soup = BS(res.content, 'html.parser')
            main_div = soup.find('div', id='pjax-job-list')
            if main_div:
                div_lst = main_div.find_all('div', attrs={'class': 'job-link'})
                for div in div_lst:
                    title = div.find('h2')
                    href = title.a['href']
                    content = div.p.text
                    company = 'No name'
                    logo = div.find('img')
                    if logo:
                        company = logo['alt']
                        jobs.append(
                            {
                                'title': title.text,
                                'url': domain + href,
                                'description': content,
                                'company': company,
                                'city_id': city,
                                'language_id': language
                            }
                        )
            else:
                errors.append({'url': url, 'title': 'Div does not exist.'})
        else:
            errors.append({'url': url, 'title': 'Page does not response.'})
    return jobs, errors

def get_hh_vacancies(url, city=None, language=None):
    res = requests.get(url, headers=headers[randint(0, 2)])
    jobs = []
    errors = []
    if url:
        if res.status_code == 200:
            soup = BS(res.content, 'html.parser')
            main_div = soup.find('div', attrs={'class': 'vacancy-serp-content'})

            if main_div:
                div_lst = main_div.find_all('div', attrs={'class': 'serp-item'})
                for div in div_lst:
                    title = div.find('h3')
                    href = title.a['href']
                    content = div.find('div', attrs={'class': 'g-user-content'})
                    responsibility = content.text
                    company = 'No name'
                    logo = div.find('div', attrs={'class': 'vacancy-serp-item__meta-info-company'})
                    if logo:
                        company = logo.a.text
                        jobs.append(
                            {
                                'title': title.text,
                                'url': href,
                                'description': responsibility,
                                'company': company,
                                'city_id': city,
                                'language_id': language
                            }
                        )
            else:
                errors.append({'url': url, 'title': 'Div does not exist.'})
        else:
            errors.append({'url': url, 'title': 'Page does not response.'})
    return jobs, errors

def get_avito_vacancies(url, city=None, language=None):
    domain = 'https://www.avito.ru'
    res = requests.get(url, headers=headers[randint(0, 2)])
    jobs = []
    errors = []
    if url:
        if res.status_code == 200:
            soup = BS(res.content, 'html.parser')
            main_div = soup.find('div', attrs={'class': 'items-items-kAJAg'})

            if main_div:
                div_lst = main_div.find_all('div', attrs={'data-marker': 'item'})
                for div in div_lst:
                    title = div.find('h3')
                    href = div.a['href']
                    content = div.find('div', attrs={'class': 'iva-item-descriptionStep-C0ty1'})
                    company = 'No name'
                    logo = div.find('div', attrs={'class': 'style-title-_wK5H text-text-LurtD text-size-s-BxGpL'})
                    if logo:
                        company = logo.text
                        jobs.append(
                            {
                                'title': title.text,
                                'url': domain + href,
                                'description': content.text,
                                'company': company,
                                'city_id': city,
                                'language_id': language
                            }
                        )
            else:
                errors.append({'url': url, 'title': 'Div does not exist.'})
        else:
            errors.append({'url': url, 'title': 'Page does not response.'})
    return jobs, errors


if __name__ == '__main__':
    # jobs, errors = get_avito_vacancies()
    # jobs, errors = get_hh_vacancies()
    # jobs, errors = get_work_ua_vacancies()
    with codecs.open('../work.txt', 'w', 'utf-8') as f:
        f.write(str(jobs))
