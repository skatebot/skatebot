import pickle
from os.path import isfile

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Bot, Update

import config
import strings


class Buttons(object):
    def __init__(self):
        if not isfile(config.reaction_data):
            with open(config.reaction_data, "wb") as f:
                pickle.dump({}, f, pickle.HIGHEST_PROTOCOL)
                f.close()
        with open(config.reaction_data, "rb") as f:
            self.datas = pickle.load(f)
            f.close()

    def save(self):
        with open(config.reaction_data, "wb") as f:
            pickle.dump(self.datas, f, pickle.HIGHEST_PROTOCOL)
            f.close()

    def new_message(self, message_id: int):
        self.datas.update(
            {message_id: dict(zip(range(len(config.reactions)), [[] for n in range(len(config.reactions))]))})
        self.save()

    def get_keyboard(self, message_id: int):
        emojis = self.datas[message_id]
        keyboard = [[]]
        for reaction in emojis:
            if not emojis[reaction]:
                keyboard[0].append(InlineKeyboardButton(config.reactions[reaction],
                                                        callback_data=f"reaction_{reaction}"))
            else:
                keyboard[0].append(InlineKeyboardButton(f"{config.reactions[reaction]} {len(emojis[reaction])}",
                                                        callback_data=f"reaction_{reaction}"))
        return keyboard

    def react(self, bot: Bot, update: Update):
        reaction_number = int(update.callback_query.data[9:])
        message_id = update.effective_message.message_id
        user_id = update.effective_user.id
        reacted_users = self.datas[message_id][reaction_number]
        if user_id not in reacted_users:
            reacted_users.append(user_id)
            bot.answer_callback_query(update.callback_query.id,
                                      strings.reacted.format(config.reactions[reaction_number]))
        else:
            reacted_users.remove(user_id)
            bot.answer_callback_query(update.callback_query.id,
                                      strings.unreacted.format(config.reactions[reaction_number]))
        keyboard = self.get_keyboard(message_id)
        bot.edit_message_reply_markup(config.channel_id, message_id, reply_markup=InlineKeyboardMarkup(keyboard))
        self.save()
