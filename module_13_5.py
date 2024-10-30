from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage = MemoryStorage())
kb = ReplyKeyboardMarkup(resize_keyboard=True)
button_start = KeyboardButton(text = 'Рассчитать')
button_info = KeyboardButton(text = 'Информация')
kb.insert(button_start)
kb.insert(button_info)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands=['start'])
async def start_message(message):
    await message.answer("Привет! Я бот помогающий твоему здоровью", reply_markup=kb)

@dp.message_handler(text='Рассчитать')
async def set_age(message):
    await message.answer('Введите свой возраст: ')
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=float(message.text))
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=float(message.text))
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=float(message.text))
    data = await state.get_data()
    await message.answer(f"Ваша норма колорий: {round(10 * data['weight'] + 6.25 * data['growth'] - 5 * data['age'] + 5, 2)}")
    await state.finish()

@dp.message_handler(text = 'Информация')
async def information(message):
    await message.answer("Это бот для расчёта колорий")

@dp.message_handler()
async def all_message(message):
    await message.answer('Введите команду /start, чтобы начать общение')



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
