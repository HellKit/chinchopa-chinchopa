import Tokens
import Parser

API_TOKEN = Tokens.TOKEN

with open('COMMANDS.txt', encoding='utf-8') as f_obj:
    COMMANDS = f_obj.readlines()

COMMANDS_LINE = ''.join(COMMANDS)


GAME_AND_ID = Parser.get_game_name_and_id()
