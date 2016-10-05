import csv
import requests
from bs4 import BeautifulSoup as BS

from dfs_report_headers import HEADERS

DEFAULT_FILE_PATH = 'data/current-ownership-proj.csv'

def scrape(file_path=DEFAULT_FILE_PATH):
    write_to_csv(scrape_ownership(), file_path)

def scrape_ownership():
    r = requests.get('https://dfsreport.com/draftkings-ownership-percentages/', headers=HEADERS)
    soup = BS(r.text, 'html.parser')
    hold = []
    for row in soup.find_all('tr'):
        if len(row.text.split('\n')) > 2:
            hold.append([row.text.split('\n')[1], row.text.split('\n')[6]])
    return hold

def write_to_csv(hold, file_path):
    with open(file_path, 'w') as fp:
        w = csv.writer(fp, delimiter=',')
        w.writerows(hold)
