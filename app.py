import time

import os
from slackclient import SlackClient

from parrots import exchange
from models import exchange_model

from util import parse_slack_output, handle_error, parrot_says, EXAMPLE_COMMAND

from requests.exceptions import ConnectionError

# Constant variables
BOT_NAME = "parrot-bot"

sc = SlackClient(os.environ["SLACK_API_TOKEN"])
        
models = [exchange_model]
parrots = [exchange.ExchangeParrot()]
parrot_cage = {}
for parrot in parrots:
    parrot_cage[parrot.NAME] = parrot.generate_actor()


def response(cmd):
    for model in models:
        if model(cmd):
            return parrot_cage[model(cmd)](cmd)
    return None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1
    if sc.rtm_connect():
        print("Parrot-Bot connected and running!")
        while True:
            try:
                command, channel = parse_slack_output(sc.rtm_read())
                if command:
                    parrot_says(response, command, channel, sc)
            except (ConnectionError,Exception) as e:
                if isinstance(e,ConnectionError):
                    print("slack refused to connect, i will sleep 5 second!")
                    sleep(5)
                else:
                    result = dict(status='error')
                    handle_error(result, channel, sc)

            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID")
