from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, \
                          KeyboardButton, InlineKeyboardButton, \
                          InlineKeyboardMarkup
import settings
from Parser.Parser import WorkshopSteam

bot = Bot(token=settings.API_TOKEN)
dp = Dispatcher(bot)

user_data = {}  # Пока что это заменяет базу данных

game_btn = KeyboardButton('Выбрать игру!')
history_btn = KeyboardButton('Посмотреть историю!')

three_buttons = ReplyKeyboardMarkup()
three_buttons.row(game_btn, history_btn)

button1 = KeyboardButton('Какая-то кнопка 1!')
button2 = KeyboardButton('Какая-то кнопка 2!')
two_buttons = ReplyKeyboardMarkup()
two_buttons.row(button1, button2)


@dp.message_handler(commands=['start', 'help'])
async def send_instruction(message: types.Message):
    if message.from_user.id not in user_data.keys():
        user_data[message.from_user.id] = [0, WorkshopSteam(), [], []]
    msg = message.text
    print(user_data, msg)
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
    print(user_data, msg)
    if msg == 'Выбрать игру!':
        game_and_id = user_data[message.from_user.id][1].get_game_name_and_id()
        game_inline = [InlineKeyboardButton(game, callback_data=f'game {game} {id_}')
                       for game, id_ in game_and_id.items()]
        inline_games_button = InlineKeyboardMarkup()
        inline_games_button.add(*game_inline)
        await message.answer('Выбирите из возможных или укажите название.',
                             reply_markup=inline_games_button)
    elif msg == 'Посмотреть историю!':
        await message.answer('Скоро тут что-то будет.')
    elif msg and user_data[message.from_user.id][0] == 1:
        user_data[message.from_user.id][0] = 0
        user_data[message.from_user.id][2].append(msg)

        user_data[message.from_user.id][1].input_to_search_panel('findItemsSearchBox',
                                                                 ' '.join(user_data[message.from_user.id][2]))
        user_data[message.from_user.id][1].click_on_button('findItemsSearchSubmit', False)
        weapons_list = [''.join([
            'StatTrak™ ' if name.startswith('StatTrak™') else '', name.split('(')[1][:-2]
        ]) for name in user_data[message.from_user.id][1].get_element_text('market_listing_item_name')]
        [user_data[message.from_user.id][3].append(elem)
         for elem in user_data[message.from_user.id][1].get_links_for_weapons('market_listing_row_link')]

        weapons_inline = [InlineKeyboardButton(weapon,
                                               callback_data=f'gun {idx}')
                          for idx, weapon in enumerate(weapons_list)]
        inline_weapon_button = InlineKeyboardMarkup()
        inline_weapon_button.add(*weapons_inline)
        await message.answer(f'{" ".join(user_data[message.from_user.id][2])}:  Выбирите качество предмета',
                             reply_markup=inline_weapon_button)
        user_data[message.from_user.id][2].clear()
    else:
        await message.answer('Может быть вы имели ввиду: /help')


@dp.callback_query_handler(lambda c: c.data.startswith('game'))
async def callback_game(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    id_ = callback_query.data.split()[2]
    game = callback_query.data.split()[1]

    user_data[callback_query.from_user.id][1].put_game_id(id_)
    user_data[callback_query.from_user.id][1].click_on_button('market_search_advanced_button')
    weapons = user_data[callback_query.from_user.id][1].get_names_of_weapons()
    user_data[callback_query.from_user.id][1].click_on_button('newmodal_close')

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
    user_data[callback_query.from_user.id][2].append(weapon)
    user_data[callback_query.from_user.id][0] = 1
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           f'{weapon}:  Введите название скина.')


@dp.callback_query_handler(lambda c: c.data.startswith('gun'))
async def callback_weapon(callback_query: types.CallbackQuery):
    weapon_id = int(callback_query.data.split()[1])
    user_data[callback_query.from_user.id][1].put_game_id(link=user_data[callback_query.from_user.id][3][weapon_id])
    price = user_data[callback_query.from_user.id][1].get_weapon_price()
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           f'Цена на {user_data[callback_query.from_user.id][3][weapon_id]} момент {price}')
    user_data[callback_query.from_user.id][3].clear()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
