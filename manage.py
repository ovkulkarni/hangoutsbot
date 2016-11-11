#!/usr/bin/env python3

from models.conversation import Conversation
from models.user import User
from models.command import Command
from models.message import Message

from hangoutsbot import HangoutsBot

from manager import Manager

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

if __name__ == '__main__':
    manager.main()
