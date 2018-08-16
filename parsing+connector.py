#_*_ coding:utf8 _*_

import psycopg2
import urllib.request
from bs4 import BeautifulSoup

# Get data
fp = urllib.request.urlopen('http://info.finance.naver.com/marketindex/exchangeList.nhn')
source = fp.read()
fp.close()
soup = BeautifulSoup(source,'html.parser')
soup = soup.find_all("td")
money_data={}
money_value=[]
for data in soup:    
    data=data.get_text().replace('\n','').replace('\t','')
    if " " in data:
        money_key=data
    else:
        money_value.append(data)
        money_data[money_key]=money_value
        if len(money_value)==6:
            money_value=[]
print(money_data)

# Connect to an existing database
host = 'localhost'
dbname = 'postgres'
user = 'postgres'
pwd = 'soso112233'
conn = psycopg2.connect('host={0} dbname={1} user={2} password={3}'.format(host, dbname, user, pwd))
cur = conn.cursor()

try:
    cur.execute("CREATE TABLE finance_list9 (country TEXT, standard TEXT, cash_buy TEXT, cash_sell TEXT, remittance_send TEXT, remittance_receipt TEXT, change_dollar TEXT);")
except:
    print('table already exists')
conn.commit()

for i in range(len(money_data)):
    country1 = list(money_data.keys())[i]
    standard1 = money_data[country1][0]
    cash_buy1 = money_data[country1][1]
    cash_sell1 = money_data[country1][2]
    remittance_send1 = money_data[country1][3]
    remittance_receipt1 = money_data[country1][4]
    change_dollar1 = money_data[country1][5]
    cur.execute("INSERT INTO finance_list9 (country, standard, cash_buy, cash_sell, remittance_send, remittance_receipt, change_dollar) VALUES (%s, %s, %s, %s, %s, %s, %s)", (country1, standard1, cash_buy1, cash_sell1, remittance_send1, remittance_receipt1, change_dollar1))
    conn.commit()

cur.execute('SELECT * FROM finance_list9;')
result = cur.fetchall()
print(result)

cur.close()
conn.close()
