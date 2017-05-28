import unittest
from parrots.weather import current_weather
def test_command():
    # Test code for new commands
    assert True

class TestWeather(unittest.TestCase):
    def test_right(self):
        assert current_weather("날씨 서울")['status'] == 'OK' 
        assert current_weather("날씨 충청북도")['status'] == 'OK'
        assert current_weather("날씨 제주도")['status'] == 'OK'
    def test_wrong(self):
        assert current_weather("날씨 으악")['status'] == 'ERROR'
        assert current_weather("날씨 센티언스")['status'] == 'ERROR'
