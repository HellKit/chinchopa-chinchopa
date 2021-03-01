from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, \
                          KeyboardButton, InlineKeyboardButton, \
                          InlineKeyboardMarkup
import settings
import Parser

bot = Bot(token=settings.API_TOKEN)
dp = Dispatcher(bot)

user_data = {} # Пока что это заменяет базу данных

game_btn = KeyboardButton('Выбрать игру!')
history_btn = KeyboardButton('Посмотреть историю!')

three_buttons = ReplyKeyboardMarkup()
three_buttons.row(game_btn, history_btn)

button1 = KeyboardButton('Какая-то кнопка 1!')
button2 = KeyboardButton('Какая-то кнопка 2!')
two_buttons = ReplyKeyboardMarkup()
two_buttons.row(button1, button2)

game_inline = [InlineKeyboardButton(game, callback_data=f'game {game} {id_}')
               for game, id_ in settings.GAME_AND_ID.items()]
inline_games_button = InlineKeyboardMarkup()
inline_games_button.add(*game_inline)


@dp.message_handler(commands=['start', 'help'])
async def send_instruction(message: types.Message):
    if message.from_user.id not in user_data.keys():
        user_data[message.from_user.id] = 0
    msg = message.text
    if not msg.startswith('/h'):
        await message.answer(f"Привет, держи кнопки для удобного пользования.\
                              \nИспользуйте {settings.COMMANDS[0]}",
                             reply_markup=three_buttons)
    else:
        await message.answer(f'Вот команды:\n\n{settings.COMMANDS_LINE}')

@dp.message_handler(commands=['traker'])
async def send_which_buttons(message: types.Message):
    await message.answer('Вот какие-то кнопки.', reply_markup=two_buttons)


@dp.message_handler()
async def main(message: types.Message):
    msg = message.text
    if msg == 'Выбрать игру!':
        await message.answer('Выбирите из возможных или укажите название.',
                             reply_markup=inline_games_button)
    elif msg == 'Посмотреть историю!':
        await message.answer('Скоро тут что-то будет.')
    elif msg and user_data[message.from_user.id] == 1:
        user_data[message.from_user.id] = 0
        qualitys = Parser.put_skin_name(msg)
        qualitys_inline = [InlineKeyboardButton(quality,
                                                callback_data=f'quality {quality}')
                         for quality in qualitys]
        inline_quality_button = InlineKeyboardMarkup()
        inline_quality_button.add(*qualitys_inline)
        await message.answer(f'{msg}:  Выбирите качество предмета',
                             reply_markup=inline_quality_button)
    else:
        await message.answer('Может быть вы имели ввиду: /help')

@dp.callback_query_handler(lambda c: c.data.startswith('game'))
async def callback_game(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    id_ = callback_query.data.split()[2]
    game = callback_query.data.split()[1]
    weapons = Parser.put_game_id(id_)
    weapon_inline = [InlineKeyboardButton(weapon, callback_data=f'weapon {weapon}')
                     for weapon in weapons]
    inline_weapon_button = InlineKeyboardMarkup()
    inline_weapon_button.add(*weapon_inline)
    await bot.send_message(callback_query.from_user.id,
                           f'{game}:  Выбирите оружие:',
                           reply_markup=inline_weapon_button)


@dp.callback_query_handler(lambda c: c.data.startswith('weapon'))
async def callback_weapon(callback_query: types.CallbackQuery):
    weapon = callback_query.data.split()[1]
    user_data[callback_query.from_user.id] = 1
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           f'{weapon}:  Введите название скина.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
