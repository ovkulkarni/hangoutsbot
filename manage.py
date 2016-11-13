#!/usr/bin/env python3

from models.conversation import Conversation
from models.user import User
from models.command import Command
from models.message import Message
from models.hook import Hook

from hangoutsbot import HangoutsBot

from manager import Manager
from colors import green

import settings

import os
import hangups
import asyncio

manager = Manager()


@manager.command
def create_tables():
    """Create the tables for the models in the database"""
    tables = [Conversation, User, Command, Message, Conversation.members.get_through_model(), Hook]
    for table in tables:
        if table.table_exists():
            print("Table already exists for {}".format(table))
        else:
            table.create_table()
            print("Created table for {}".format(table))


@manager.command
def run():
    """Run HangoutsBot"""
    bot = HangoutsBot()
    bot.run()


@manager.command
def shell():
    """Open python shell with context"""
    print(green(">>> from database import database"))
    print(green(">>> from models.conversation import Conversation"))
    print(green(">>> from models.user import User"))
    print(green(">>> from models.command import Command"))
    print(green(">>> from models.message import Message"))
    print(green(">>> from models.hook import Hook"))
    os.system(
        "python -i -c '"
        "from database import database;"
        "from models.conversation import Conversation;"
        "from models.user import User;"
        "from models.command import Command;"
        "from models.message import Message;"
        "from models.hook import Hook;'"
    )


@manager.command
def get_bot_id():
    """Get ID of Bot Account to put in secret.py"""
    client = hangups.client.Client(hangups.auth.get_auth_stdin(settings.COOKIES_FILE_PATH))
    client.on_connect.add_observer(lambda: asyncio.async(get_id(client)))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(client.connect())


@asyncio.coroutine
def get_id(client):
    request = hangups.hangouts_pb2.GetSelfInfoRequest(
        request_header=client.get_request_header(),
    )
    try:
        response = yield from client.get_self_info(request)
        print(response.self_entity.id.gaia_id)
    finally:
        yield from client.disconnect()


if __name__ == '__main__':
    manager.main()
