# Constant variables
import os
BOT_NAME = "parrot-bot"
BOT_ID = os.environ["BOT_ID"]
AT_BOT = "<@" + BOT_ID + ">"


def get_bot_id(sc):
    api_call = sc.api_call("users.list")
    if api_call.get('ok'):
        # retrieve all users so we can find our bot
        users = api_call.get('members')
        for user in users:
            if 'name' in user and user.get('name') == BOT_NAME:
                print("Bot ID for '" + user['name'] + "' is " + user.get('id'))
    else:
        print("could not find bot user with the name " + BOT_NAME)

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

def handle_error(sc):
    response = "(local)뭐라는거야. 이런 명령어를 쓰도록 해 *" + EXAMPLE_COMMAND + "*"
    sc.api_call("chat.postMessage", channel=channel, text=response, as_user=True)

def parrot_says(result, channel, sc):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """

    EXAMPLE_COMMAND = "환율"
    response = "뭐라는거야. 이런 명령어를 쓰도록 해 *" + EXAMPLE_COMMAND + "*"
    if result['status'] == 'OK':
        response = "현재 환율은 {} 이래 :fastparrot:".format(result['data'])
    else:
        response = "음...뭔가 잘못 입력한게 아닐까? :sadparrot:"

    sc.api_call("chat.postMessage", channel=channel, text=response, as_user=True)
    return print("Post message")

 
