from Parrot import Parrot
from parrots import exchange,weather
parrot = Parrot()

@parrot.route("환율")
def exchange_func(command):
    ex = exchange.ExchangeParrot()
    return ex.generate_actor()(command)
    #지금은 이전 구조에 맞춰져서 이렇게 변태같이 씀.
    #나중엔 class일 필요 없이 함수로 간단히 쓸 수 있을듯.
@parrot.route("날씨")
def weather_controller(command):
    return weather.current_weather(command)

parrot.run()
