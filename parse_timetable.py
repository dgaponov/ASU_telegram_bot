import csv
import re
import urllib.request
from bs4 import BeautifulSoup

BASE_URLS = []
i = 10
while i <= 39:
    BASE_URLS.append('http://www.asu.ru/timetable/students/' + str(i) + '/')
    i += 1

def get_html(url):
    response = urllib.request.urlopen(url)
    return response.read()

def parse_group(html):
    soup = BeautifulSoup(html, "lxml")
    table = soup.find_all('tr', class_='schedule-time')
    pairs = []
    for i in table:
            colm = i.find_all('td')
            try:
                data = colm[5].find('a')['href'][27:35]
            except:
                print('exc')
            try:
                pairs.append({
                    'date': data,
                    'number_pair': colm[0].text.strip(),
                    'subject': re.sub('\s+',' ', colm[2].text).strip(),
                    'teacher': re.sub('\s+',' ', colm[3].text).strip(),
                    'class': re.sub('\s+',' ', colm[4].text).strip()
                })
            except:
                print('exc2')
    return pairs

def save(pairs, path):
    with open(path, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(('Дата', 'Номер пары', 'Предмет', 'Преподаватель', 'Кабинет'))
        for pair in pairs:
            writer.writerow((pair['date'], pair['number_pair'], pair['subject'], pair['teacher'], pair['class']))

def parse_groups(html):
    soup = BeautifulSoup(html, "lxml")
    table = soup.find_all('div', class_='link_ptr_left margin_bottom')
    groups = []
    for group in table:
        groups.append({'number': group.find('a').text,
                       'url': group.find('a')['href']})
    return groups

def main():
    for faculty in BASE_URLS:
        for group in parse_groups(get_html(faculty)):
            save(parse_group(get_html(faculty + group['url'])), group['number'] + '.csv')

if __name__ == '__main__':
    main()