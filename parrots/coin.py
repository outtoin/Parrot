from selenium import webdriver
from bs4 import BeautifulSoup

from time import time

import json
 
class CoinParrot:
    URI = "https://www.bithumb.com/"
    NAME = 'coin'

    def _get_coin_exchange(self, command):
        driver = webdriver.PhantomJS()

        driver.get(self.URI)

        html = driver.page_source

        bs = BeautifulSoup(html, "html.parser")

        table = bs.find('table', attrs={'class': 'g_table'})
        tbody = table.find('tbody')
        rows = tbody.find_all('tr')

        result = []

        for row in rows:
            cols = row.find_all('td')
            cols = [element.text.strip() for element in cols]
            data = dict(
                coinName=cols[0],
                coinPrice=cols[1],
                coinPriceChange=cols[2],
                coinPriceChange_pm=cols[2].split(' ')[0] if len(
                    cols[2].split(' ')) > 4 else 0,
                coinPriceChange_num=cols[2].split(' ')[1] if len(
                    cols[2].split(' ')) > 4 else 0,
                coinPriceChange_percent=cols[2].split(' ')[4] if len(
                    cols[2].split(' ')) > 4 else 0
            )
            result.append(data)

        res = {}
        if len(result) > 0:
            attachments = []
            for data in result:

                if data['coinPriceChange_pm'] == '+' and float(data['coinPriceChange_percent']) > 5:
                    color = "good"
                elif data['coinPriceChange_pm'] == '-' and float(data['coinPriceChange_percent']) > 5:
                    color = "danger"
                else:
                    color = "warning"

                attachment = {
                    "title": data['coinName'],
                    "text": data['coinPrice'],
                    "color": color,
                    "fields": [
                        {
                            "title": '24시간 변동량',
                            "value": data['coinPriceChange_pm'] +
                            data['coinPriceChange_num'] + "원",
                            "short": 'true'
                        },
                        {
                            "title": '24시간 변동률(%)',
                            "value": data['coinPriceChange_pm'] +
                            data['coinPriceChange_percent'] + "%",
                            "short": 'true'
                        }
                    ],
                    "footer": "Parrot",
                    "ts": time()
                }

                attachments.append(attachment)

            res['status'] = 'OK'
            res['message'] = attachments

            return res

        else:
            res['status'] = 'undefined'
            res['message'] = '음...뭔가 잘못 입력한게 아닐까? :sadparrot:'
            return res

    def generate_actor(self):
        def _actor(command):
            return self._get_coin_exchange(command)
        return _actor
