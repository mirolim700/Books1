from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from main import db


# oddiy usul
menu = ReplyKeyboardMarkup(
	keyboard = [
		[
		KeyboardButton(text="Kitoblar"),
		KeyboardButton(text="Qidirish")
		],
		[
		KeyboardButton(text="Aloqa")
		],
	],resize_keyboard=True
)

# tsikl
async def for_category_get_all():
	x = db.select_category_all()
	print(x)
	categories = InlineKeyboardMarkup(row_width=2)
	for i in x:
		button_text = i[1]
		callback_data = i[0]
		categories.insert(
			InlineKeyboardButton(text=button_text,callback_data=f"productall_{callback_data}")
			)
	return categories

# tsikl
async def get_category_id(id):
	x = db.select_products_for_category_id(id)
	print(x)
	products = InlineKeyboardMarkup(row_width=2)
	for i in x:
		button_text = i[2]
		callback_data = i[0]
		products.insert(
			InlineKeyboardButton(text=button_text,callback_data=f"products_{callback_data}")
			)
	return products

async def search_books(suz):
	x = db.search_product(suz)
	print(x)
	products = InlineKeyboardMarkup(row_width=2)
	for i in x:
		button_text = i[2]
		callback_data = i[0]
		products.insert(
			InlineKeyboardButton(text=button_text,callback_data=f"products_{callback_data}")
			)
	return products

		