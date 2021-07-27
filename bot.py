#!/usr/bin/env python

import logging
from api_endpoints import getTokenAPI, getPoolAPI

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

help_text = "Use a slash <pre>/</pre> to declare pairs. Ex. <code>/liq CEL/ETH</code>"


def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Liquidation bot online.')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text(help_text, parse_mode="HTML")


def getTokens(update, context):
    """Sends API requires for tokens"""
    user_text = update.message.text[4:].strip()

    if (' ' in user_text) or (not '/' in user_text):
        update.message.reply_text(help_text, parse_mode='HTML')
        return

    requestedToken = user_text.split("/")[0].upper()
    requestedPool = user_text.split("/")[1].upper()

    tokenAPI_reply = getTokenAPI(requestedToken)
    if(not tokenAPI_reply):
        update.message.reply_text("Token not found")
        return

    tokenAPI_reply = tokenAPI_reply[0]

    poolAPI_reply = getPoolAPI(
        tokenAPI_reply['id'], tokenAPI_reply['symbol'], requestedPool)

    if (not poolAPI_reply):
        update.message.reply_text("Pool not found")

    logger.info(poolAPI_reply)

    poolAPI_reply = poolAPI_reply[0]

    short_id = "{}...{}".format(
        poolAPI_reply['id'][0:4], poolAPI_reply['id'][-4:])

    update.message.reply_text("Uniswap Liquidation for {} \nTVL: ${:,}\nFee Tier: {}%\n<a href='{}'>{}</a>".format(
        user_text,
        round(float(
            poolAPI_reply['totalValueLockedUSD']), 2),
        round(int(poolAPI_reply['feeTier'])/10000, 2),
        "https://info.uniswap.org/#/pools/{}".format(poolAPI_reply["id"]),
        short_id),
        parse_mode='HTML')


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    updater = Updater(
        "", use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("liq", getTokens))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
