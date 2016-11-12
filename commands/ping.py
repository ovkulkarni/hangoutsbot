from utils.commands import BaseCommand
from utils.parser import parser

import asyncio


class Ping(BaseCommand):

    def __init__(self, config, parser, admin_required):
        super(Ping, self).__init__(name, config, parser, admin_required)

    @asyncio.coroutine
    def run(self, bot, conversation, user, args):
        parsed = self.parser.parse_known_args(args)
        yield from bot.send_message(conversation, " ".join(parsed[1]))

command = Ping(parser, {}, False)
