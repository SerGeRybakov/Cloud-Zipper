"""*Задача №2(необязательная)
Самый важный сайт для программистов это stackoverflow. И у него тоже есть API Нужно написать программу, которая 
выводит все вопросы за последние два дня и содержит тэг 'Python'. Для этого задания токен не требуется."""


import time
import datetime
import requests as r


URL = "https://api.stackexchange.com/2.2/questions"

# unix date
now = int(time.mktime(datetime.date.today().timetuple()))
then = now - 86400 * 2

params = {
    "fromdate": then,
    "todate": now,
    "sort": "creation",
    "tagged": "python",
    "order": "desc",
    "page": 1,
    "pagesize": 100,
    "site": "stackoverflow",
}

questions = []
resp = r.get(URL, params=params)
for item in resp.json()['items']:
    questions.append(item['title'])

while len(resp.json()['items']) == 100:
    params["page"] += 1
    resp = r.get(URL, params=params)
    for item in resp.json()['items']:
        questions.append(item['title'])
for question in enumerate(questions):
    print(question[0]+1, question[1])
