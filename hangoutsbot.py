#!/usr/bin/env python3

import logging
import asyncio
import os
import sys
import hangups

import settings

from models.user import User
from models.conversation import Conversation
from models.message import Message

from utils.commands import register_commands
from utils.enums import EventType, ConversationType

from datetime import datetime

# main log
logger = logging.getLogger(__name__)
logging.basicConfig(format="%(levelname)s: %(asctime)s | %(message)s")
logger.setLevel(logging.DEBUG)

# messages log
message_formatter = logging.Formatter('[%(message_time)s] <%(username)s> %(message)s')
file_handler = logging.FileHandler('bot_messages.log')
file_handler.setFormatter(message_formatter)
message_logger = logging.getLogger("message_logger")
message_logger.setLevel(logging.INFO)
message_logger.addHandler(file_handler)


class HangoutsBot(object):

    def __init__(self):
        register_commands()
        self.client = hangups.client.Client(self.login())

    def login(self):
        return hangups.auth.get_auth_stdin(settings.COOKIES_FILE_PATH)

    def run(self):
        logger.debug(self.client)
        self.client.on_state_update.add_observer(self.handle_update)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.client.connect())

    @asyncio.coroutine
    def handle_update(self, state_update):
        logger.debug("Handling event update")
        if state_update.event_notification.event.event_type == EventType.EVENT_TYPE_REGULAR_CHAT_MESSAGE.value:
            yield from self.handle_message(state_update)
        # elif state_update.event_notification.event.type == EventType.EVENT_TYPE_ADD_USER:
        #    yield from self.handle_user_added(state_update)
        # elif state_update.event_notification.event.type == EventType.EVENT_TYPE_REMOVE_USER:
        #    yield from self.handle_user_removed(state_update)
        else:
            pass

    @asyncio.coroutine
    def handle_message(self, state_update):
        logger.debug("Handling message")
        if state_update.event_notification.event.sender_id.gaia_id == settings.BOT_ID:
            return True
        conversation = self.get_or_create_conversation(state_update.conversation)
        self.check_conversation_participants(state_update.conversation)
        try:
            sending_user = User.get(User.id == state_update.event_notification.event.sender_id.gaia_id)
        except User.DoesNotExist:
            user_id = state_update.event_notification.event.sender_id.gaia_id
            sending_user = self.create_user_from_id(user_id, state_update.conversation)
        message_body = ""
        for seg in state_update.event_notification.event.chat_message.message_content.segment:
            message_body += seg.text
        message = Message.create(conversation=conversation, user=sending_user, text=message_body, time=datetime.now())
        message_logger.info(message.text, extra={
            "username": message.user.username,
            "message_time": datetime.strftime(message.time, "%X"),
        })
        return True

    def create_user_from_id(self, user_id, conversation):
        logger.debug("Creating User with id {}".format(user_id))
        participant_object = None
        for participant in conversation.participant_data:
            if participant.id.gaia_id == user_id:
                participant_object = participant
                break
        name_split = participant_object.fallback_name.split(" ", 1)
        if len(name_split) > 1:
            user = User.create(id=user_id, first_name=name_split[0], last_name=name_split[1])
        else:
            user = User.create(id=user_id, first_name=name_split[0], last_name="")
        return user

    def get_or_create_conversation(self, conversation):
        logger.debug("Creating Conversation with id {}".format(conversation.conversation_id.id))
        try:
            conv = Conversation.get(Conversation.id == conversation.conversation_id.id)
        except Conversation.DoesNotExist:
            is_group = conversation.type == ConversationType.CONVERSATION_TYPE_GROUP.value
            conv = Conversation.create(id=conversation.conversation_id.id, group=is_group)
        return conv

    def check_conversation_participants(self, conversation):
        logger.debug("Checking Conversation participants")
        conv = self.get_or_create_conversation(conversation)
        for participant in conversation.participant_data:
            try:
                user = User.get(User.id == participant.id.gaia_id)
            except User.DoesNotExist:
                user = self.create_user_from_id(participant.id.gaia_id, conversation)
            if user not in conv.members:
                logger.debug("Adding User {} to Conversation {}".format(user.id, conv.id))
                conv.members.add(user)
        return True

if __name__ == "__main__":
    print("Run the bot using the manage.py file: ./manage.py run")
