from asyncio import run as asyncio_run
from os import getenv
from telebot.async_telebot import AsyncTeleBot
from dotenv import load_dotenv


load_dotenv()
BOT_TOKEN = getenv("BOT_TOKEN")
STICKER_ID = "CAACAgQAAxkBAAEQXlVpeziVedqPHniBLqApYq8DsLb1aAACTAEAAqghIQZjKrRWscYWyDgE"
WELCOME_MESSAGE = \
    "Приветствую, {name}! Данный бот будет отправлять тебе каждый день список праздников, которые можно отпраздновать." \
    "\nБот поддерживает следующие команды:" \
    "\n🔸 <code>/help</code>" \
    "\n🔸 <code>/today_holiday</code>" \
    "\n🔸 <code>/unsubscribe</code>"
HELP_MESSAGE = \
    "Данный бот раз в день отправляет сообщение со списком праздников, которые проходят в данный день. " \
    "Если вы хотите отписаться от рассылки выполните команду: <code>/unsubscribe</code>. " \
    "Вы так же можете самостоятельно запросить список празников, выполнив команду: <code>/today_holiday</code>." \
    "\n<b>Другой функционал в боте не предусмотрен </b>."


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
    await bot.send_message(chat_id, WELCOME_MESSAGE.format(name=first_name), parse_mode='HTML')
    await bot.send_sticker(chat_id, STICKER_ID)

@bot.message_handler(commands=["help"])
async def send_help_message(message):
    chat_id = await get_data(message, chat_id_only=True)
    await bot.send_message(chat_id, HELP_MESSAGE, parse_mode='HTML')

@bot.message_handler()
async def reply(message):
    chat_id = await get_data(message, chat_id_only=True)
    await bot.send_message(chat_id, HELP_MESSAGE, parse_mode='HTML')


print("Бот начал работу")
asyncio_run(bot.polling())