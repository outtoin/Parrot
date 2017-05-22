import time

import os
from slackclient import SlackClient

from parrots import exchange
from models import exchange_model

from util import parse_slack_output, handle_error, parrot_says, EXAMPLE_COMMAND

# Constant variables
BOT_NAME = "parrot-bot"

sc = SlackClient(os.environ["SLACK_API_TOKEN"])
        
models = [exchange_model]
parrots = [exchange.ExchangeParrot()]
parrot_cage = {}
for parrot in parrots:
    parrot_cage[parrot.NAME] = parrot.generate_actor()


def response(command):
    for model in models:
        if model(command):
            return parrot_cage[model(command)](command)
    return None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1
    if sc.rtm_connect():
        print("Parrot-Bot connected and running!")
        while True:
            try:
                command, channel = parse_slack_output(sc.rtm_read())
                success = 0 # if all model failed, command is not valid

                result = response(command)
                if result:
                    if result['status'] == 'OK':
                        parrot_says(result, channel, sc)
                    else:
                        handle_error(result, channel, sc)
                else:
                    result = dict(status='error', message='뭐라는거야. 이런 명령어를 쓰도록 해 *' + EXAMPLE_COMMAND + "*")
                    handle_error(result, channel, sc)  # if command is '', handle_error wouldn't be executed
            except:
                result = dict(status='error')
                handle_error(result, channel, sc)

            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID")
