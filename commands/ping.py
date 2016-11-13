from models.command import BaseCommand
from utils.parser import parser
from utils.textutils import spacing
import asyncio


class Ping(BaseCommand):

    def __init__(self, name, parser, admin_required):
        super(Ping, self).__init__(name, parser, admin_required)

    @asyncio.coroutine
    def run(self, bot, conversation, user, args):
        parsed = self.parser.parse_known_args(args)
        if len(parsed[1]) == 0:
            parsed[1].append("pong")
        message = " ".join(parsed[1])
        yield from bot.send_message(conversation, message, parsed[0].filter)

command = Ping("ping", parser, False)
