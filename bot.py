from asyncio import run as asyncio_run
from os import getenv
from telebot.async_telebot import AsyncTeleBot
from dotenv import load_dotenv

from database import DataBase


load_dotenv()
BOT_TOKEN = getenv("BOT_TOKEN")
WELCOME_STICKER_ID = "CAACAgQAAxkBAAEQXlVpeziVedqPHniBLqApYq8DsLb1aAACTAEAAqghIQZjKrRWscYWyDgE"
UNSUBSCRIPTION_STICKER_ID = "CAACAgQAAxkBAAEQXr9pe2JReqJBpf9NrCB6SDLOrCffYQACCQkAAjDeSVM1hjr988KC5TgE"
SUBSCRIPTION_STICKER_ID = "CAACAgQAAxkBAAEQXsFpe2KVrGwujjPtUr4z-QXCBUBDyAACMwEAAqghIQaDngab6f9thTgE"
WELCOME_MESSAGE = \
    "Приветствую, {name}! Данный бот будет отправлять тебе каждый день список праздников, которые можно отпраздновать." \
    "\nБот поддерживает следующие команды:" \
    "\n🔸 <code>/help</code>" \
    "\n🔸 <code>/today_holiday</code>" \
    "\n🔸 <code>/subscribe</code>" \
    "\n🔸 <code>/unsubscribe</code>"
HELP_MESSAGE = \
    "Данный бот раз в день отправляет сообщение со списком праздников, которые проходят в данный день. " \
    "Если вы хотите отписаться от рассылки выполните команду: <code>/unsubscribe</code>, " \
    "а для восстановления рассылки - команду:  <code>/subscribe</code>. " \
    "Вы так же можете самостоятельно запросить список празников, выполнив команду: <code>/today_holiday</code>." \
    "\n<b>Другой функционал в боте не предусмотрен </b>."
UNSUBSCRIPTION_MESSAGE = "{name}, вы успешно отписались от рассылки!\nЕсли захотите вновь получать сообщения о праздниках - выполните поманду <code>/subscribe</code>."
SUBSCRIPTION_MESSAGE = "{name}, вы успешно подписались на рассылку!\nЕё можно отменить в любое время, выполнив поманду <code>/unsubscribe</code>."


async def get_data(message: dict, chat_id_only: bool = False) -> tuple[int, str, str, str] | int:
    chat_id = message.chat.id
    if not chat_id_only:
        first_name = message.chat.first_name
        last_name = message.chat.last_name
        username = message.chat.username
        return chat_id, first_name, last_name, username
    else:
        return chat_id


bot = AsyncTeleBot(BOT_TOKEN)


@bot.message_handler(commands=["start"])
async def send_welcome_message(message):
    chat_id, first_name, last_name, username = await get_data(message)
    DataBase.add_new_user(chat_id, first_name, last_name, username)
    await bot.send_message(chat_id, WELCOME_MESSAGE.format(name=first_name), parse_mode='HTML')
    await bot.send_sticker(chat_id, WELCOME_STICKER_ID)

@bot.message_handler(commands=["help"])
async def send_help_message(message):
    chat_id = await get_data(message, chat_id_only=True)
    await bot.send_message(chat_id, HELP_MESSAGE, parse_mode='HTML')

@bot.message_handler(commands=["today_holiday"])
async def send_today_holiday(message):
    chat_id = await get_data(message, chat_id_only=True)
    user_name = DataBase.get_user_name(chat_id)
    await bot.send_message(chat_id, f"Твое имя: {user_name}")

@bot.message_handler(commands=["unsubscribe"])
async def unsubscribe(message):
    chat_id = await get_data(message, chat_id_only=True)
    user_name = DataBase.change_subscription(chat_id, is_subscription=False)
    await bot.send_message(chat_id, UNSUBSCRIPTION_MESSAGE.format(name=user_name), parse_mode='HTML')
    await bot.send_sticker(chat_id, UNSUBSCRIPTION_STICKER_ID)

@bot.message_handler(commands=["subscribe"])
async def subscribe(message):
    chat_id = await get_data(message, chat_id_only=True)
    user_name = DataBase.change_subscription(chat_id, is_subscription=True)
    await bot.send_message(chat_id, SUBSCRIPTION_MESSAGE.format(name=user_name), parse_mode='HTML')
    await bot.send_sticker(chat_id, SUBSCRIPTION_STICKER_ID)

@bot.message_handler()
async def reply(message):
    chat_id = await get_data(message, chat_id_only=True)
    await bot.send_message(chat_id, HELP_MESSAGE, parse_mode='HTML')


print("Бот начал работу")
asyncio_run(bot.polling())