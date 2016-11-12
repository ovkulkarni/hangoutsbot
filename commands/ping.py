from models.command import BaseCommand
from utils.parser import parser

import asyncio


class Ping(BaseCommand):

    def __init__(self, name, config, parser, admin_required):
        super(Ping, self).__init__(name, config, parser, admin_required)

    @asyncio.coroutine
    def run(self, bot, conversation, user, args):
        parsed = self.parser.parse_known_args(args)
        if len(parsed[1]) == 0:
            parsed[1].append("pong")
        yield from bot.send_message(conversation, " ".join(parsed[1]))

command = Ping("ping", {}, parser, True)
