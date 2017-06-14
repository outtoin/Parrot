import os
import time
import re
from slackclient import SlackClient

from app.util import parrot_says, handle_error, parse_slack_output

class Bot(object):

    def __init__(self):
        self.patterns = {}
        self.sc = SlackClient(os.environ["SLACK_API_TOKEN"])

    def route(self, pattern, **kwargs):
        """
            route: register pattern-app to self.patterns dictionary
        """
        def _wrapper_(f):
            self.patterns[pattern] = {'function':f, 'kwargs':kwargs}
            return f
        return _wrapper_

    def _pattern_matcher(self, pattern, command):
        """
            pattern_matcher: abstraction of pattern(command)-application matching

            QnA
                Q: Why did you pull out this? it seems not that complicate.
                A: It because pattern_matching procedure would be more complex than today.
                    e.g. NLP, ....
        """
        return re.match(pattern, command)

    def run(self):
        READ_WEBSOCKET_DELAY = 1
        if self.sc.rtm_connect():
            print("Parrot-Bot connected and running!")
            while True:
                try:
                    command, channel = parse_slack_output(self.sc.rtm_read())
                    if command:
                        for pattern in self.patterns: # iterate registered(by route decorator) patterns
                            if self._pattern_matcher(pattern, command):
                                parrot_says(self.patterns[pattern]['function'], command, channel, self.sc, **self.patterns[pattern]['kwargs'])
                except (ConnectionError,Exception) as e:
                    if isinstance(e,ConnectionError):# e.g. slack timeout(or refuse)
                        print("slack refused to connect, i will sleep 5 second!")
                        sleep(5)
                    else:
                        result = dict(status='error')
                        handle_error(result, channel, self.sc)

                time.sleep(READ_WEBSOCKET_DELAY)
        else:
            print("Connection failed. Invalid Slack token or bot ID")
