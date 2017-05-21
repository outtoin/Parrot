from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup


class ExchangeParrot:
    URI = "http://info.finance.naver.com/marketindex/exchangeList.nhn"
    NAME = 'exchange'
    def _parser(self,command):
        return command.replace('환율 ','')
    def _get_exchange(self,country):
        """
        Tells the exchange rate of each country
        :return: json array
        """
        try:
            html = urlopen(self.URI)
            bs = BeautifulSoup(html, "html.parser")

            table = bs.find('table', attrs={'class': 'tbl_exchange'})
            table_body = table.find('tbody')
            rows = table_body.find_all('tr')
            result = []

            for row in rows:
                cols = row.find_all('td')
                cols = [element.text.strip() for element in cols]
                data = dict(
                    currency=cols[0],
                    TradingRate=cols[1],
                    Buy=cols[2],
                    Sell=cols[3],
                    Transfer=cols[4],
                    Receiver=cols[5],
                    ConversionRate=cols[6]
                )
                result.append(data)

            result = [each['Buy'] for each in result if country in each['currency']]
            res = {}
            if len(result) > 0:
                res['status'] = 'OK'
                res['data'] = result[0]
                return res
            else:
                res['status'] = 'undefined'
                return res

        except HTTPError as e:
            print(e)
            return None

    def generate_actor(self):
        def _actor(command):
            country = self._parser(command)
            return self._get_exchange(country)
        return _actor
