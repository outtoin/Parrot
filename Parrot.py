import time
import re
import os
from slackclient import SlackClient
from util import handle_error, parse_slack_output, parrot_says

EXAMPLE_COMMAND = "환율"
class Parrot:

    def __init__(self):
        self.sc = SlackClient(os.environ["SLACK_API_TOKEN"])
        self.patterns = {} 

    def route(self, pattern):
        """
        Parrot.route
        description:
            route certain pattern to controller(function)
        usage:
            @parrot.route("pattern")
            def func(command): # decorated func must support command argument!
                ...
        happening:
            if you decorated certain function, it register the function in patterns dictionary
            the dictionary looks like:
                {
                    "pattern" : controller # function 
                    ...
                }
        """
        def wrapper(controller):
            self.patterns[pattern] = controller 
            return controller 
        return wrapper 

    def response(self, command):
        """
        Parrot.response
        description:
            check every pattern.
            if it is matched to input command, 
            trigger function at self.patterns[pattern].
            command would be arguemnt of the funciton.
        output:
            usually, 
                command, channel
            but it doesn't ensure what the output is.
        """
        for pattern in self.patterns:
            if isinstance(command, str) and re.match(pattern, command):
                return self.patterns[pattern](command)
        return None
    def run(self):
        READ_WEBSOCKET_DELAY = 1
        if self.sc.rtm_connect():
            print("Parrot-Bot connected and running!")
            while True:
                command, channel = parse_slack_output(self.sc.rtm_read())
                try:
                    result = self.response(command)
                    if result:
                        if result['status'] == 'OK':
                            parrot_says(result, channel, self.sc)
                        else:
                            handle_error(result, channel, self.sc)
                    else:
                        result = dict(status='error', message='뭐라는거야. 이런 명령어를 쓰도록 해 *' + EXAMPLE_COMMAND + "*")
                        handle_error(result, channel, self.sc)  # if command is '', handle_error wouldn't be executed
                except Exception as e:
                    result = dict(status='error')
                    handle_error(result, channel, self.sc)

                time.sleep(READ_WEBSOCKET_DELAY)
        else:
            print("Connection failed. Invalid Slack token or bot ID")
