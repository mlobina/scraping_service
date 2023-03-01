import asyncio
import codecs
import os, sys



proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)

os.environ['DJANGO_SETTINGS_MODULE'] = 'scraping_service.settings'

import django
django.setup()
from django.contrib.auth import get_user_model
from django.db import DatabaseError
from scraping.parsers import *
from scraping.models import City, Error, Language, Vacancy, Url

User = get_user_model()

parsers = (
    (get_work_ua_vacancies, 'work'),
    (get_hh_vacancies, 'hh'),
    (get_avito_vacancies,
     'avito')
)

jobs, errors = [], []

def get_settings():
    qs = User.objects.filter(send_email=True).values() # список словарей со свойствами каждого объекта в qs
    settings_st = set((q['city_id'], q['language_id']) for q in qs) # set из кортежей (city_id, language_id) для users
    return settings_st

def get_urls(_settings):
    qs = Url.objects.all().values()
    url_dct = {(q['city_id'], q['language_id']): q['url_data'] for q in qs}
    urls = []
    for pair in _settings:
        tmp = {}
        tmp['city'] = pair[0]
        tmp['language'] = pair[1]
        url_data = url_dct.get(pair)
        if url_data:
            tmp['url_data'] = url_dct.get(pair)
            urls.append(tmp)
    return urls


settings = get_settings()
url_list = get_urls(settings)


async def main(value):
    func, url, city, language = value
    job, err = await loop.run_in_executor(None, func, url, city, language )
    jobs.extend(job)
    errors.extend(err)

loop = asyncio.get_event_loop()
tmp_tasks = [
             (parser, data['url_data'][key], data['city'], data['language'])
             for data in url_list
             for parser, key in parsers
            ]
tasks = asyncio.wait([loop.create_task(main(f)) for f in tmp_tasks])

# for data in url_list:
#
#     for parser, key in parsers:
#         url = data['url_data'][key]
#         j, e = parser(url, city=data['city'], language=data['language'])
#         jobs += j
#         errors += e

loop.run_until_complete(tasks)
loop.close

for job in jobs:
    v = Vacancy(**job)
    try:
        v.save()
    except DatabaseError:
        pass
if errors:
    er = Error(data=errors).save()

# with codecs.open('../work.txt', 'w', 'utf-8') as f:
#     f.write(str(jobs))
