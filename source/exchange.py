from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup



class ExchangeParrot:
    URI = "http://info.finance.naver.com/marketindex/exchangeList.nhn"
    NAME = 'exchange'
    def __init__(self,sc):
        self.sc = sc
    def _parser(self,command):
        return command.replace('환율 ','')
    def _get_exchange(self,country,channel):
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
            exchange = result[0] if len(result) >0 else "undefined"
            response = "(local)현재 환율이래 {} :fastparrot:".format(exchange)
            self.sc.api_call("chat.postMessage", channel=channel, text=response, as_user=True)
            return print("Post message")


        except HTTPError as e:
            print(e)
            return None

    def generate_actor(self):
        def _actor(command,channel):
            country = self._parser(command)
            return self._get_exchange(country,channel)
        return _actor
