# coding: utf-8
import requests
import json
from bs4 import BeautifulSoup as bs
from datetime import date, timedelta
from os import environ
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(BASE_DIR, "bank_envs.json")) as f:
    envs = json.loads(f.read())

def get_env(setting, envs):
    return envs[setting]


class Transaction(object):
    def __init__(self):
        try:
            # TODO: you should export envs before execute!
            self.residentnumber = get_env('RESIDENTNUMBER',envs)
            self.bankid = get_env('BANKID',envs)
            self.password = get_env('BANKPW',envs)
            self.accountnumber = get_env('ACCOUNTNUMBER',envs)
        except KeyError:
            print("TODO: you should export envs before execute!")

    @property
    def check_transactions(self):
        url = 'https://obank.kbstar.com/quics?asfilecode=524517&_FILE_NAME=KB_거래내역빠른조회.html&USER_TYPE=02&주민사업자번호=000000{residentnumber}&고객식별번호={bankid}&조회구분=2&_LANG_TYPE=KOR&비밀번호={password}&조회시작일={startday}&응답방법=2&다음거래일련번호키=&조회종료일={endday}&다음거래년월일키=&계좌번호={accountnumber}'.format(
            residentnumber= self.residentnumber, #주민번호 뒷자리
            bankid= self.bankid.upper(), #인터넷 뱅킹 ID
            password= self.password, #계좌 비밀번호
            startday= (date.today()-timedelta(1)).strftime("%Y%m%d"), #조회시작일/어제
            endday= date.today().strftime("%Y%m%d"), #조회마감일/오늘
            accountnumber= self.accountnumber #계좌번호
        )
        with requests.Session() as s:
            res = s.get(url)
            if res == '':
                raise Exception('반환받은 결과가 없음')
            html = res.text
            soup = bs(html, 'html.parser')
            infos = soup.select('tr[align:center] > td')
            item_quantitys = int(len(infos)) / 9
            item_seq = 0
            transactions = []
            while item_seq < item_quantitys:
                transaction = []
                seq = infos[item_seq*9:item_seq*9+8]
                for i in seq:
                    transaction.append(i.text.strip())
                transactions.append(transaction)
                item_seq += 1
            return transactions

    @property
    def get_transact_dic(self):
        results = self.check_transactions
        result_dics = []
        for info in results:
            transact_date = info[0].strip()[:10]
            transact_time = info[0].strip()[10:]
            transact_by = info[2].strip()
            if info[4] != '0':
                transact_amount = "-" + info[4].strip()
            else:
                transact_amount = "+" + info[5].strip()
            print("거래일시: {}\n거래시각: {}\n​거래처: {}\n거래금액: {}".format(
                transact_date, transact_time, transact_by, transact_amount
            ))
            result_dics.append({
                'date': transact_date,
                'time': transact_time,
                'by': transact_by,
                'amount': transact_amount
            })
        return result_dics