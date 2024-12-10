import json

import requests
from bs4 import BeautifulSoup

url = "https://www.time.ir/fa/eventyear-%d8%aa%d9%82%d9%88%db%8c%d9%85-%d8%b3%d8%a7%d9%84%db%8c%d8%a7%d9%86%d9%87"

page = requests.get(url)

soup = BeautifulSoup(page.content, 'html.parser')

year = []

for month in soup.find_all('div', class_='eventsCurrentMonthWrapper'):
    month_data = {
        "month": {
            "name": "",
            "holidays": []
        }
    }
    month_data["month"]["name"] = month.find('div', class_='eventsCurrentMonthTitle').text.strip()
    event_holidays = month.find_all('li', class_='eventHoliday')
    for event in event_holidays:
        holiday_data = {
            "date": event.find('span').text.strip(),
            "ocation": event.contents[2].strip()
        }
        month_data["month"]["holidays"].append(holiday_data)

    year.append(month_data)

json_output = json.dumps(year, ensure_ascii=False, indent=4)
print(json_output)