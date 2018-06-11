"""
util functions for paintbot
"""
import signal
from functools import (
    wraps
)
from paintbot.globals import (
    BOT_TIMELIMIT,
    BOT_TIMEOUT_MESSAGE
)


class BotTimeout(Exception):
    """bot timed out"""


def paintbot(func):
    """decorator for the bot runs, adding a timeout"""
    def __timeout(signum, frame):
        """handle the timeout event"""
        raise BotTimeout(BOT_TIMEOUT_MESSAGE)

    @wraps(func)
    def wrapper(*args, **kwargs):
        """wrapper function for timing out a bot"""
        signal.signal(signal.SIGALRM, __timeout)
        signal.alarm(BOT_TIMELIMIT)
        try:
            result = func(*args, **kwargs)
        finally:
            signal.alarm(0)
        return result
    return wrapper
