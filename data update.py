#_*_ coding:utf8 _*_

import psycopg2
import urllib.request
import time
from bs4 import BeautifulSoup

def crawling():
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
    return money_data

def return_value(money_data):
    contry = input("나라: ")
    for name in list(money_data.keys()):
        if contry in name:
            standard1 = money_data[name][0]
            cash_buy1 = money_data[name][1]
            cash_sell1 = money_data[name][2]
            remittance_send1 = money_data[name][3]
            remittance_receipt1 = money_data[name][4]
            change_dollar1 = money_data[name][5]
    print("매매 기준율: ", standard1)
    print("현찰(사실 때): ", cash_buy1)
    print("현찰(파실 때): ", cash_sell1)
    print("송금(보내실 때): ", remittance_send1)
    print("송금(받으실 때): ", remittance_receipt1)
    print("미화환산율: ", change_dollar1)

def connector(money_data):
    host = 'localhost'
    dbname = 'postgres'
    user = 'postgres'
    pwd = 'soso112233'
    conn = psycopg2.connect('host={0} dbname={1} user={2} password={3}'.format(host, dbname, user, pwd))
    cur = conn.cursor()

    cur.execute('DROP TABLE finance_list;')
    cur.execute("CREATE TABLE finance_list (country TEXT, standard TEXT, cash_buy TEXT, cash_sell TEXT, remittance_send TEXT, remittance_receipt TEXT, change_dollar TEXT);")
    conn.commit()
    for i in range(len(money_data)):
        country1 = list(money_data.keys())[i]
        standard1 = money_data[country1][0]
        cash_buy1 = money_data[country1][1]
        cash_sell1 = money_data[country1][2]
        remittance_send1 = money_data[country1][3]
        remittance_receipt1 = money_data[country1][4]
        change_dollar1 = money_data[country1][5]
        cur.execute("INSERT INTO finance_list (country, standard, cash_buy, cash_sell, remittance_send, remittance_receipt, change_dollar) VALUES (%s, %s, %s, %s, %s, %s, %s)", (country1, standard1, cash_buy1, cash_sell1, remittance_send1, remittance_receipt1, change_dollar1))
        conn.commit()
    cur.close()
    conn.close()



while True:
    money_data1 = crawling()
    time.sleep(10)
    money_data2 = crawling()
    if (money_data1!=money_data2):
        print(money_data2)
        connector(money_data2)


