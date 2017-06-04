from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from bs4 import BeautifulSoup


class CoinParrot:
    URI = "https://www.bithumb.com/"
    NAME = 'coin'

    def _get_coin_exchange(self, command):
        driver = webdriver.PhantomJS()

        '''
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, 'g_table')))

        except TimeoutException as ex:
            print (ex.message)
            res = {}
            res['status'] = 'error'
            res['message'] = '뭔가 문제가 있는 것 같아..:explodyparrot:'
            return res
        '''

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
            text = []
            for data in result:
                rowData = data['coinName'] + ": " + \
                    data['coinPrice'] + "(" + data['coinPriceChange'] + ")"

                if data['coinPriceChange_pm'] == '+' and float(data['coinPriceChange_percent']) > 5:
                    rowData = '*' + rowData + '*'
                elif data['coinPriceChange_pm'] == '-' and float(data['coinPriceChange_percent']) > 5:
                    rowData = '_' + rowData + '_'

                text.append(rowData)

            resText = ""
            for line in text:
                resText = resText + line + "\n"

            res['status'] = 'OK'
            res['message'] = '*현재시세* : \n' + resText + ":fastparrot:"

            return res

        else:
            res['status'] = 'undefined'
            res['message'] = '음...뭔가 잘못 입력한게 아닐까? :sadparrot:'
            return res

    def generate_actor(self):
        def _actor(command):
            return self._get_coin_exchange(command)
        return _actor
