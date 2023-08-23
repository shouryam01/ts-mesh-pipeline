import pandas as pd
from bs4 import BeautifulSoup
import re
import requests
class Scrap:
    def __init__(self, url):
        self.url = url

    def eprocure(self):
        result = requests.get(self.url)
        result
        soup = BeautifulSoup(result.text, 'html.parser')
        rows1 = []
        
        table1 = soup.find('table', id = 'activeTenders')
        for rows in table1.find_all('tr'):
            data = rows.find_all('td')
            rows1.append([td.text for td in data])
            
        df = pd.DataFrame(rows1)
        
        table2 = soup.find('table', id = 'activeCorrigendums')
        rows2 = []
        for rows in table2.find_all('tr'):
            data = rows.find_all('td')
            rows2.append([td.text for td in data])
            
        headers = []
        for row in soup.find_all('tr', class_ = 'list_header'):
            data = row.find_all('td')
            headers.append([td.text for td in data])
            
        df1 = pd.DataFrame(rows1, columns = headers[0])
        df2 = pd.DataFrame(rows2, columns = headers[2])
        
        df1['Tender Title'] = df1['Tender Title'].apply(lambda x: re.sub('\d. ', '', x))
        df2['Corrigendum Title'] = df2['Corrigendum Title'].apply(lambda x: re.sub('\d. ', '', x))
        return [df1, df2]