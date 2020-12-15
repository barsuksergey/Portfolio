import pandas as pd
import datetime as dt
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from bs4 import BeautifulSoup
import re

def converter(x):
    if type(x) == str:
        if bool(re.match(r'\d+(?:\.)\d+%', x)) == True:
            return float(x[:-1])/100
        elif bool(re.match(r'\d+(?:\.)\d+[A-Z]', x)) == True:
            if x[-1] == 'T':
                return float(x[:-1])*10e11
            elif x[-1] == 'B':
                return float(x[:-1])*10e8
            elif x[-1] == 'M':
                return float(x[:-1])*10e5
            else:
                return str(x)
        elif bool(re.match(r'\d+(?:\.)\d+$', x)) == True:
            return float(x)
        else:
            return str(x)
    else:
        return str(x)
                

class Ticker:
    def __init__(self, index):
        self.index = index.upper()
    
    def profile(self):
        url = f'https://finance.media.yahoo.com/quote/{self.index}?p={self.index}'
        dfs = pd.read_html(url, match = '.+')
        frames = [dfs[0],dfs[1]]
        data = pd.concat(frames)
        data.columns = ['KPI', 'value']
        data['value'] = data['value'].apply(lambda x: converter(x))
        data = data.reset_index().drop('index', axis =1).set_index('KPI')
        
        return data
    
    def key_stats(self):
        url = f'https://finance.media.yahoo.com/quote/{self.index}/key-statistics?p={self.index}'
        dfs = pd.read_html(url, match = '.+')
        data = pd.DataFrame()
        frames = [dfs[x] for x in range(1,len(dfs))]
        data = data.append(frames)
        data.columns = ['KPI', 'value']
        data['value'] = data['value'].apply(lambda x: converter(x))
        data = data.reset_index().drop('index', axis =1).set_index('KPI')
        
        return data


    def val_measures(self):
        url = f'https://finance.media.yahoo.com/quote/{self.index}/key-statistics?p={self.index}'
        dfs = pd.read_html(url, match = '.+')
        data = dfs[0]
        data.rename(columns = {data.columns[0] : 'KPI'}, inplace = True)
        data = data.reset_index().drop('index', axis =1).set_index('KPI')
        for x in range(len(data.columns)):
            data.iloc[x] = data.iloc[x].apply(lambda x: converter(x))
        for x in range(len(data.columns)):
            data.iloc[x] = data.iloc[x].astype(float)
        
        return data

    def get_history(self, date_from=str(dt.date.today() - dt.timedelta(days=7)), date_to=str(dt.date.today()), set_sleep = 1):
        """ This function gets URL from Yahoo Fin, deafult date from: a week ago, date to: today. Dates are format YYYY-MM-DD.
        set_sleep is number seconds used to control the time your browser needs to load each update on page, do not set too quick """
        date_from = dt.datetime.strptime(date_from, '%Y-%m-%d')
        date_to = dt.datetime.strptime(date_to, '%Y-%m-%d')
        unix_to = int(dt.datetime(date_to.year,date_to.month,date_to.day).replace(tzinfo=dt.timezone.utc).timestamp())
        unix_from = int(dt.datetime(date_from.year,date_from.month,date_from.day).replace(tzinfo=dt.timezone.utc).timestamp())
        url = f'https://ca.finance.yahoo.com/quote/{self.index}/history?period1={unix_from}&period2={unix_to}&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true'
        browser = webdriver.Chrome()
        browser.implicitly_wait(3)
        browser.get(url)
        html = browser.find_element_by_tag_name('html')
        old_rows = browser.execute_script("return document.getElementsByTagName('tr').length")
        while True:
            html.send_keys(Keys.END)
            sleep(set_sleep)
            new_rows = browser.execute_script("return document.getElementsByTagName('tr').length")
            if old_rows == new_rows:
                break
            else:
                old_rows = new_rows

        page_source = browser.page_source
        
        soup = BeautifulSoup(page_source, features = 'lxml')
        table = soup.find('table', {"class":"W(100%)"})
        rows = table.findAll('tr')
        headers = [rows[0].findAll('th')[x].text for x in range(len(rows[0].findAll('th')))]

        row_list = []
        for r in range(1,len(rows)):
            get_row = [rows[r].findAll('td')[x].text for x in range(len(rows[r].findAll('td')))]
            row_list.append(get_row)
            data = pd.DataFrame(data = row_list, columns = headers)
        
        for x in range(1,len(data.columns)):
            data.iloc[:,x] = data.iloc[:,x].str.replace(',', '').astype(float)
        data = data.drop([len(data)-1])
        data.iloc[:,0] = pd.to_datetime(data.iloc[:,0])
        
        return data
