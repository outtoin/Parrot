from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup


URI = "http://info.finance.naver.com/marketindex/exchangeList.nhn"


def get_exchange():
    """
    Tells the exchange rate of each country
    :return: json array
    """
    try:
        html = urlopen(URI)
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
        return result

    except HTTPError as e:
        print(e)
        return None