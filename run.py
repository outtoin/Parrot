from app import Bot
from parrots import exchange, coin
bot = Bot()

@bot.route("환율")
def currency(command):
    ex = exchange.ExchangeParrot()
    return ex.generate_actor()(command)

@bot.route("coin",attachments=True)
def Coin(command):
    co = coin.CoinParrot()
    return co.generate_actor()(command)

bot.run()
