# TODO: Парсер

def get_game_name_and_id():
    games = ['CS:GO']
    links = ['730']
    games_with_id = {game: link for game, link in zip(games, links)}
    return games_with_id


def put_game_id(id_):
    # TODO: Поиск по ссылке
    print(f'Ссылка на игру: https://steamcommunity.com/market/search?appid={id_}')
    names_weapon = ['AWP', 'AK-47', 'Deagle']
    return names_weapon


def put_skin_name(skin):
    # TODO:  Поиск скина по определенной игре
    print(f'Выбраный скин: {skin}')
    qualitys = ['Закаленное в боях', 'Поношенное', 'После полевых испытаний',
                'Немного поношенно', 'Прямо из завода']
    return qualitys
