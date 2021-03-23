import Tokens
from Parser.Parser import WorkshopSteam

API_TOKEN = Tokens.TOKEN

with open('COMMANDS.txt', encoding='utf-8') as f_obj:
    COMMANDS = f_obj.readlines()

COMMANDS_LINE = ''.join(COMMANDS)
