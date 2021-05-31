import Tokens
from DataBase import UserData
import sqlite3 as sql

with open('COMMANDS.txt', encoding='utf-8') as f_obj:
    COMMANDS = f_obj.readlines()

COMMANDS_LINE = ''.join(COMMANDS)
API_TOKEN = Tokens.TOKEN
DATA_BASE = UserData.DataBase()
try:
    DATA_BASE.create_tables()
except sql.OperationalError:
    print('Table exists')


def check_black_list(id_):
    black_list = [437557320]
    if id_ in black_list: return False
    return True
