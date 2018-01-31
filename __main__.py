import logging

from telegram import Bot, Update, InlineKeyboardMarkup
from telegram.ext import Updater, CallbackQueryHandler, CommandHandler

import config
import reaction_buttons
import strings
import twitter_api

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

BUTTONS = reaction_buttons.Buttons()
TWITTER = twitter_api.Twitter()


def start(bot: Bot, update: Update):
    bot.send_message(update.effective_chat.id, strings.start)


def send_latest_messages(bot: Bot, job):
    tweets = TWITTER.get_new_tweets()
    if tweets:
        for tweet in tweets:
            print(tweet)
            message = bot.send_message(config.channel_id, tweet.full_text, parse_mode="HTML")
            BUTTONS.new_message(message.message_id)
            keyboard = BUTTONS.get_keyboard(message.message_id)
            bot.edit_message_reply_markup(config.channel_id, message.message_id,
                                          reply_markup=InlineKeyboardMarkup(keyboard))


updater = Updater(config.token)
updater.bot.delete_webhook()
updater.dispatcher.add_handler(CallbackQueryHandler(BUTTONS.react, pattern=r"^reaction_\d$"))
updater.dispatcher.add_handler(CommandHandler("start", start))
updater.job_queue.run_repeating(send_latest_messages, config.twitter_polling, first=config.twitter_polling)
updater.start_polling(config.telegram_polling)
updater.idle()
