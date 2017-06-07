from app import Bot
from parrots import exchange 
bot = Bot()

@bot.route("환율")
def currency(command):
    ex = exchange.ExchangeParrot()
    return ex.generate_actor()(command)

bot.run()
