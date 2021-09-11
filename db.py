import sqlite3
from mocks import User


class DataBase:

    def __init__(self, db_name="users.db"):
        self.name = db_name
        conn = self.__get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""CREATE TABLE users (
                    tg_id integer,
                    first_name text,
                    username text,
                    last_name text, 
                    language_code text, 
                    supports_inline_queries null,
                    registration_date integer,
                    remove_bg_api_key text
                )
                """)
            conn.commit()
            conn.close()
        except Exception as e:
            conn.close()
            print("[!]", e.args[0])

    def __get_connection(self):
        return sqlite3.connect(self.name)

    def user_not_exist(self, user: User):
        if self.find(user) is None:
            return True
        else:
            return False

    def add(self, user: User):
        conn = self.__get_connection()
        cursor = conn.cursor()
        user_data = tuple(user)
        cursor.execute(f"INSERT INTO users VALUES (?,?,?,?,?,?,?,?)", user_data)
        conn.commit()
        conn.close()

    def find(self, user: User):
        conn = self.__get_connection()
        cursor = conn.cursor()
        user = cursor.execute(f"SELECT * FROM users WHERE tg_id='{user.tg_id}'")
        user_tuple = user.fetchone()
        user = User(tuple_=user_tuple)
        return user

    def update(self, user: User):
        conn = self.__get_connection()
        cursor = conn.cursor()
        cursor.execute(f"""UPDATE users SET remove_bg_api_key='{user.api_key}' WHERE tg_id='{user.tg_id}'""")
        conn.commit()
        conn.close()


if __name__ == "__main__":
    db = DataBase()

