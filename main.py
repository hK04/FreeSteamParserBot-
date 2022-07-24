import logging 
import asyncio 
from aiogram import Bot, Dispatcher, executor, types
from aiogram.bot import api

from config_ import TOKEN
from users_db_ import DB_users
from parser_ import Parser

# keyboard example 
'''
def get_kb_1():
	keyboard = types.InlineKeyboardMarkup()
	keyboard.add(
		types.InlineKeyboardButton(text=test", callback_data="test"),
		types.InlineKeyboardButton(text="test", callback_data="test"))
	keyboard.add(
		types.InlineKeyboardButton(text="test", callback_data="test")
		)
	return keyboard
'''
def auth():
	global DB,PARS
	DB = DB_users()
	DB.close_db()
	PARS = Parser()
def get_kb():
	keyboard = types.InlineKeyboardMarkup()
	keyboard.add(
		types.InlineKeyboardButton(text="ДА✔", callback_data="YES"))
	return keyboard
def get_kb_c():
	keyboard = types.InlineKeyboardMarkup()
	keyboard.add(
		types.InlineKeyboardButton(text="ПРЕКРАТИТЬ РАССЫЛКУ?🚫", callback_data="SUSPEND"))
	return keyboard
def get_kb_c1():
	keyboard = types.InlineKeyboardMarkup()
	keyboard.add(
		types.InlineKeyboardButton(text="ВЕРНУТЬ РАССЫЛКУ?✔", callback_data="CONTINUE"))
	return keyboard

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PATCHED_URL = "https://telegg.ru/orig/bot{token}/{method}"
setattr(api, "API_URL", PATCHED_URL)

bot = Bot(token = TOKEN,)
dp = Dispatcher(bot = bot,)

	
@dp.message_handler(commands = ['start'])
async def m_handler(message: types.Message):
	await bot.send_message(message.chat.id, "Приветствую, желаете подписатся на рассылку о новых бесплатных играх?",
		reply_markup=get_kb())
@dp.callback_query_handler()
async def c_handler(callback):
	global DB
	if callback.data == 'YES':
		DB.conect()
		print(callback.message.chat.id)
		DB.db_add_user(callback.message.chat.id)
		DB.close_db()
		await bot.send_message(callback.message.chat.id, "Отлично!")
	elif callback.data == 'SUSPEND':
		DB.conect()
		DB.change_status(callback.message.chat.id, 'off')
		DB.close_db()
		await  bot.edit_message_text(chat_id = callback.message.chat.id, message_id = callback.message.message_id, text = callback.message.text)
		await bot.send_message(callback.message.chat.id, "Рассылка приостановлена ;(", reply_markup=get_kb_c1())
	elif callback.data == 'CONTINUE':		
		DB.conect()
		DB.change_status(callback.message.chat.id, 'on')
		DB.close_db()
		await bot.delete_message(chat_id = callback.message.chat.id, message_id = callback.message.message_id)
		await bot.send_message(callback.message.chat.id, "Вы вернулись на рассылку! ;)", reply_markup=get_kb_c())

async def scheduled(wait_for):
	global DB, PARS
	while 1:
		await asyncio.sleep(wait_for)
		DB.conect()
		S,a,u,i,t = PARS.update_and_check()
		text = '*'+a+'*\n'+t
		if S:
			for j in DB.get_list_of_users():
				await bot.send_message(j[0],text,parse_mode='Markdown',reply_markup=get_kb_c())
				#await bot.send_photo(j[0],i)


		DB.close_db()
if __name__ == '__main__':
	auth()
	dp.loop.create_task(scheduled(10))
	executor.start_polling(dispatcher=dp)