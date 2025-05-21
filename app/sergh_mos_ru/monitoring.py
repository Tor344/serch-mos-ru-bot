import requests
import json
def s(url):
    response = requests.get(url=url)
    print(response.text)

s("https://tickets.mos.ru/widget/api/widget/performance_free_seats?date_from=2025-05-19&date_to=2028-05-19&event_id=65305")