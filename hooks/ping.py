import asyncio


class PingHook(object):

    def __init__(self, name, regex):
        self.name = name
        self.regex = regex

    @asyncio.coroutine
    def run(self, bot, conversation, user, text):
        yield from bot.send_message(conversation, "pong")

hook = PingHook("ping", ".*(ping).*")
