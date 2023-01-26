"""
This is a echo bot.
It echoes any incoming text messages.
"""

import logging

from baza import Database


from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text 
from buttons import *


# for state
from aiogram.contrib.fsm_storage.memory import MemoryStorage  #for temporary memory
from aiogram.dispatcher import FSMContext #for state
from state import StateData,Search #from state file calling state
from config import API_TOKEN, admin

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage()) #temporary memory
db=Database()
db.create_category()
db.create_table_sub_products()
db.create_users()


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    tg_id = message.from_user.id 
    name = message.from_user.first_name
    users_ = db.select_users(tg_id)
    if users_:
        await message.reply("Assalomu aleykum Elektron kutuxonaga xush kelibsiz\nQuyidagilardan birini tanlang",reply_markup=menu)
    else:
        db.insert_users(tg_id,name)
        await message.reply("Assalomu aleykum Elektron kutuxonaga xush kelibsiz\nQuyidagilardan birini tanlang",reply_markup=menu)


@dp.message_handler(text="Kitoblar")
async def send_welcome(message: types.Message):
    markup = await for_category_get_all()
    await message.reply("Bo'limlaridan birini tanlang!",reply_markup=markup)

@dp.message_handler(text="Qidirish",state="*")
async def send_welcome(message: types.Message,state=FSMContext):
    await message.reply("Qidirish uchun kitob nomini kiriting!")
    await state.set_state(Search.product_search)
# search_product
@dp.message_handler(state=Search.product_search)
async def send_welcome(message: types.Message,state=FSMContext):
    await state.update_data(product_search=message.text)

    data = await state.get_data()
    search_ = data.get("product_search")


    await state.finish()
    await state.reset_state()
    products=await search_books(search_)
    await message.answer("Qidiruv un mos kitoblar",reply_markup=products)

@dp.message_handler(text="Aloqa")
async def send_welcome(message: types.Message):
    await message.answer("Murojat va takliflar uchun: @mirolim700")

@dp.callback_query_handler(Text(startswith="productall_"))
async def send_welcome(call: types.CallbackQuery):
    index = call.data.index('_')
    id = call.data[index+1:]
    products = await get_category_id(id)
    await call.message.reply("Kitoblardan birini tanlang!",reply_markup=products)

@dp.callback_query_handler(Text(startswith="products_"))
async def send_welcome(call: types.CallbackQuery):
    index = call.data.index('_')
    id = call.data[index+1:]
    product = db.select_product_id(id)
    # await call.message.answer(f"Siz tanlangan kitob\nKitob nomi: {product[3]}\nKitob haqida: {product[4]}")
    await call.message.answer_photo(photo=product[4], caption=f"{product[2]}\n{product[3]}")
    await call.message.answer_document(document=product[-1])

# Product add
@dp.message_handler(commands=['add_product'],state="*",user_id=admin)
async def product_add(message: types.Message, state: FSMContext):
    await message.answer("Kitob nomini kiriting")
    await state.set_state(StateData.product_name)

# number_of_users
@dp.message_handler(commands=['users'],user_id=admin)
async def users_count(message: types.Message):
    data = db.users_count()
    await message.answer(f"Foydalanuchilar soni : {data[0]}")
# for product_name
@dp.message_handler(state=StateData.product_name)
async def product(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await message.answer("Kitob nomini matn korinishida kiriting!")
        return
    await state.update_data(product_name=message.text)
    await message.answer("Kitobning category idsini kiriting")
    await StateData.next()


@dp.message_handler(state=StateData.product_category_id)
async def product(message: types.Message, state: FSMContext):
    if message.text.isalpha():
        await message.answer("Kitob category idsini son korinishida kiriting!")
        return
    await state.update_data(product_category_id=message.text)
    await message.answer("Kitob haqida ma'lumot kiriting")
    await StateData.next()


@dp.message_handler(state=StateData.product_des)
async def send_welcome(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await message.answer("Kitob haqida ma'lumotni matn korinishida kiriting!")
        return
    await state.update_data(product_des=message.text)
    await message.answer("Kitobning rasmni kiriting")
    await StateData.next()

@dp.message_handler(content_types = "any", state=StateData.product_photo)
async def send_welcome(message: types.Message, state: FSMContext):
    if message.content_type != "photo":
        await message.answer("Kitobni rasmni png yoki jpg format korinishida kiriting!")
        return
    await state.update_data(product_photo=message.photo[-1]["file_id"])
    await message.answer("Kitobning faylni kiriting")
    await StateData.next()

@dp.message_handler(content_types = "any", state=StateData.product_file_id)
async def send_welcome(message: types.Message, state: FSMContext):
    if message.content_type != "document":
        await message.answer("Kitobni pdf yoki boshqa dokument format korinishida kiriting!")
        return
    await state.update_data(product_file_id=message.document["file_id"])

    data = await state.get_data()
    name_ = data.get("product_name")
    category_id_ = data.get("product_category_id")
    des_ = data.get("product_des")
    photo_ = data.get("product_photo")
    file_id_ = data.get("product_file_id")

    db.insert_products(name_, category_id_, des_, photo_, file_id_)

    await state.finish()
    await state.reset_state()
    await message.answer("Ma'lumotlar saqlandi!")



@dp.message_handler()
async def echo(message: types.Message): 
    # old style:
    # await bot.send_message(message.chat.id, message.text)

    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)