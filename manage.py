#!/usr/bin/env python3

from models.conversation import Conversation
from models.user import User
from models.command import Command
from models.message import Message

from hangoutsbot import HangoutsBot

from manager import Manager
from colors import green

import os

manager = Manager()


@manager.command
def create_tables():
    """Create the tables for the models in the database"""
    tables = [Conversation, User, Command, Message, Conversation.members.get_through_model()]
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
    os.system(
        "python -i -c '"
        "from database import database;"
        "from models.conversation import Conversation;"
        "from models.user import User;"
        "from models.command import Command;"
        "from models.message import Message;'"
    )

if __name__ == '__main__':
    manager.main()
