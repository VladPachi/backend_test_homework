import requests  # библиотека для API
import json  # билиотека для JSON
from datetime import datetime  # для определния сегодняшней даты
import csv  # для записи в CSV
import pygsheets  # https://github.com/nithinmurali/pygsheets для Gsheets

url = "https://api.topvisor.com/v2/json/get/keywords_2/keywords"

headers = {'User-Id': '244398',
           'Authorization': "4efd432f20fe02af262f",
           'Content-type': 'application/json'
           }
day = '2022-06-01'  # datetime.today().strftime('%Y-%m-%d')  # сегодня в формате 'yyyy-mm-dd'
data = {
    'project_id': 3541348,
    'fields': ['name',
               f'position:{day}:3541348:1',  # вывод позиций: дата, project_id, region_index
               'volume:213:0:3'  # вывод частоты: регион номер ПС, номер вида частоты
               ],
    "orders": [{
        "name": "volume:213:0:3",
        "direction": "DESC"
        }],
    "filters": [
        {  # фильтр по частоте
            "name": "volume:213:0:3",
            "operator": "GREATER_THAN_EQUALS",
            "values": [1] 
            },
        {  # фильтр по позиции
            "name": f'position:{day}:3541348:1',
            "operator": "LESS_THAN",
            "values": [30]
            },
        {  # фильтр по содержанию в ключе
            "name": 'name',
            "operator": "DOES_NOT_CONTAIN",
            "values": ['кодир'] 
            }
        ]
    }

data_json = json.dumps(data)  # перевод в json
response = requests.post(url, headers=headers, data=data_json)
response = json.loads(response.text)  # перевод обратно в питон
#  дальше работа с данными _________
result = response['result']


def add_to_csv(file, name):
    """Функция для записи данных в файл"""

    with open(str(name)+'.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        for row in file:
            writer.writerow(row)
    with open(str(name)+'.csv') as f:
        print('Файл ' + name + ' успешно создан')


gc = pygsheets.authorize(
    service_file="D:/Dev/Скрипт все сразу/for-python-336508-356967b65c6b.json")


def add_to_Gsheet(file, key, p):
    sz = len(file)

    if sz == 0:
        return
    sh = gc.open_by_key(key)
    wks = sh.sheet1
    diap = str(
        '=ИНДЕКС($F$1:$F$' + str(sz)+'; СЛУЧМЕЖДУ(1;' + str(sz) +'))'
        )
    wks.update_values('F:', file)
    wks.update_value('A1', diap)
    wks.update_value('E1', p)
    print('Данные в таблице успешно обновлены ссылка: '
          + 'https://docs.google.com/spreadsheets/d/' + key)
    print(f'Необходимое количество выполнений квеста {str(p)}')


def kpower(spisok):
    """Подсчет количества повторений и кол-ва показов."""
    chst = []
    for i in spisok:
        chst.append(i[1])
    return (1 / min(chst))
def pov(spisok):
    chst = []
    for i in spisok:
        chst.append(i[1])
    return (round(sum(chst)/90))
def stroki(file):
    s = []
    for i in file:
        c = (round(i[1]*kpower(file)))
        if c < 1:
            c=1
        for j in range(c):
            s.append([i[0]])
    return(s)

#______
#запросы  на сегменты      
result500 = []
result100 = []
result20 = []
result0= []

for l in result:
    if l.get(data['fields'][2]) >= 500:
        result500.append([l.get(data['fields'][0],'--'),l.get(data['fields'][2],'--')])
    elif l.get(data['fields'][2]) >= 100 and l.get(data['fields'][2]) <500:
        result100.append([l.get(data['fields'][0],'--'),l.get(data['fields'][2],'--')])
    elif l.get(data['fields'][2]) >= 20 and l.get(data['fields'][2]) <100:
        result20.append([l.get(data['fields'][0],'--'),l.get(data['fields'][2],'--')])
    elif l.get(data['fields'][2]) >= 1 and l.get(data['fields'][2]) <20:
        result0.append([l.get(data['fields'][0],'--'),l.get(data['fields'][2],'--')])

#запросы 500+            
add_to_Gsheet(stroki(result500), "1ZIdunVBR_Oj2DgZ6uv9ztWAegUtvWucCBIRo9D_8XlU", pov(result500))

#запросы  100 -500

add_to_Gsheet(stroki(result100), "1aCvUo3xLY4u7lBp5Z8qMddfcxscqPfzshbWhm6Cve9o", pov(result100))

#Запросы 20 - 100

add_to_Gsheet(stroki(result20), "1e375XVHEKoc9jBySwG1RLm6Rgh5yo-PXM28B07rfX_U", pov(result20))

#запросы <20

add_to_Gsheet(stroki(result0), "1JEkbBgYgdEkJ_-K_4dTPuo6rjDYRXyGABF6RScAcblU", pov(result0))
