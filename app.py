import os
import time
from slackclient import SlackClient
from source import exchange

# Constant variables
BOT_ID = os.environ["BOT_ID"]
AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "환율"
BOT_NAME = "parrot-bot"

sc = SlackClient(os.environ["SLACK_API_TOKEN"])


def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = "뭐라는거야. 이런 명령어를 쓰도록 해 *" + EXAMPLE_COMMAND + "*"
    if command.startswith(EXAMPLE_COMMAND):
        result = exchange.get_exchange(command)

        if result['status'] == 'OK':
            response = "현재 환율은 {} 이래 :fastparrot:".format(result['data'])

        else:
            response = "음...뭔가 잘못 입력한게 아닐까? :sadparrot:"

    sc.api_call("chat.postMessage", channel=channel, text=response, as_user=True)
    return print("Post message")


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1
    if sc.rtm_connect():
        print("Parrot-Bot connected and running!")
        while True:
            command, channel = parse_slack_output(sc.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID")