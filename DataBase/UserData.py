import sqlite3 as sql


class MainDataBase:
    def __init__(self):
        self._connect = sql.connect('../User.db')
        self._cursor = self._connect.cursor()

    def __create_users(self):
        query = """CREATE TABLE Users (id INT NOT NULL PRIMARY KEY, 
                                       weapon_ INT NOT NULL)"""
        self._cursor.execute(query)

    def __create_users_urls_to_weapons(self):
        query = """CREATE TABLE UsersUrlsToWeapons (weapon_name VARCHAR(250) NOT NULL UNIQUE, 
                                                    url_to_weapon VARCHAR(500) NOT NULL)"""
        self._cursor.execute(query)

    def __create_users_to_weapons(self):
        query = """CREATE TABLE UsersToWeapons (user_id INT NOT NULL, 
                                                weapon_id INT NOT NULL, 
                                                FOREIGN KEY (user_id) REFERENCES Users(id), 
                                                FOREIGN KEY (weapon_id) REFERENCES UsersUrlsToWeapons(rowid))"""
        self._cursor.execute(query)

    def create_tables(self):
        self.__create_users()
        self.__create_users_urls_to_weapons()
        self.__create_users_to_weapons()


class DBaseUser(MainDataBase):
    def __init__(self):
        super().__init__()

    def create_user_id(self, user_id: int):
        query = f"""INSERT INTO Users (id, weapon_) 
                    VALUES ({int(user_id)}, 0)"""
        self._cursor.execute(query)
        self._connect.commit()

    def create_weapon_status(self, user_id: int, weapon_status: int):
        query = f"""UPDATE Users 
                    SET weapon_ = {int(weapon_status)} 
                    WHERE id = {int(user_id)}"""
        self._cursor.execute(query)
        self._connect.commit()

    def get_all_users(self):
        query = """SELECT * 
                   FROM Users"""
        data = self._cursor.execute(query)
        print([*data])

    def check_user_in(self, user_id: int):
        query = f"""SELECT id
                    FROM Users 
                    WHERE id = {int(user_id)}"""
        data = self._cursor.execute(query)
        return [*data]


class UsersUrlsToWeapon(MainDataBase):
    def __init__(self):
        super().__init__()

    def create_weapon_and_url(self, name_: str, url_: str):
        query = f"""INSERT INTO UsersUrlsToWeapons (weapon_name, url_to_weapon) 
                    VALUES ('{name_}', '{url_}')"""
        self._cursor.execute(query)
        self._connect.commit()

    def get_all_weapon_and_url(self):
        query = """SELECT * 
                   FROM UsersUrlsToWeapons"""
        data = self._cursor.execute(query)
        return [*data]

    def get_row_id(self, weapon_name: str):
        query = f"""SELECT rowid 
                    FROM UsersUrlsToWeapons 
                    WHERE weapon_name='{weapon_name}'"""
        data = self._cursor.execute(query).fetchone()
        return data[0] if data else []

    def check_weapon(self, weapon_name: str):
        return self.get_row_id(weapon_name=weapon_name)

    def get_url(self, weapon_name: str):
        query = f"""SELECT url_to_weapon 
                    FROM UsersUrlsToWeapons 
                    WHERE weapon_name='{weapon_name}'"""
        data = self._cursor.execute(query).fetchone()
        return data[0] if data else []


class UsersToWeapon(MainDataBase):
    def __init__(self):
        super().__init__()

    def get_all_users_and_url(self):
        query = """SELECT * 
                   FROM UsersToWeapons"""
        data = self._cursor.execute(query)
        print([*data])

    def create_user_id_and_weapon_id(self, user_id: int, weapon_id: int):
        query = f"""INSERT INTO UsersToWeapons (user_id, weapon_id) 
                    VALUES ({int(user_id)}, {int(weapon_id)})"""
        self._cursor.execute(query)
        self._connect.commit()

    def get_history(self, user_id: int):
        query = f"""SELECT DISTINCT t2.weapon_name as name, t2.url_to_weapon as weapon
                    FROM (SELECT t2.weapon_id as weapon_id
                          FROM Users t1
                          JOIN UsersToWeapons t2
                          ON t1.id = {user_id}) t1
                    LEFT JOIN UsersUrlsToWeapons t2
                    ORDER BY name DESC LIMIT 5"""
        data = self._cursor.execute(query)
        return {name[0]: name[1] for name in [*data]} if data else []


class DataBase(DBaseUser,
               UsersUrlsToWeapon,
               UsersToWeapon):
    def __init__(self):
        super().__init__()


# DATA_BASE = DataBase()


# if __name__ == '__main__':
#     bd = DataBase()
#     try:
#         bd.create_tables()
#     except sql.OperationalError:
#         print('Table exists')
#     id_ = input('user id: ')
#     print(bd.get_history(id_))
#     if not bd.check_user_in(id_):
#         bd.create_user_id(user_id=id_)
#     bd.create_weapon_status(user_id=id_, weapon_status=0)
#     bd.get_all_users()
#     name_ = input('Weapon name: ')
#     if not bd.check_weapon(name_):
#         url_ = input('Url: ')
#         bd.create_weapon_and_url(name_=name_, url_=url_)
#     id_weapon = bd.get_row_id(name_)
#     if id_weapon:
#         bd.create_user_id_and_weapon_id(user_id=id_, weapon_id=id_weapon)
#     bd.get_all_weapon_and_url()
#     bd.get_all_users_and_url()
#     url = bd.get_url(name_)
#     print(url)
#



