from aiogram.dispatcher.filters.state import StatesGroup,State

class StateData(StatesGroup):
	product_name=State()
	product_category_id=State()
	product_des=State()
	product_photo=State()
	product_file_id=State()
class Search(StatesGroup):
	product_search=State()
