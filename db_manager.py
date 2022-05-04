import sqlite3
import os.path

import logging

db_logger = logging.getLogger('db_logger')


class DBManager:

    def __init__(self, path):
        if not os.path.exists(path):
            raise FileNotFoundError("File not found. Try again")

        self.connect = sqlite3.connect(path)
        self.cursor = self.connect.cursor()
        self.user_counter = 0

    def user_exists(self, user_id):
        result = self.cursor.execute("SELECT id FROM users WHERE user_id=?", (user_id,))
        return bool(result.fetchall())

    def add_user(self, user_id):
        if not self.user_exists(user_id):
            self.cursor.execute("INSERT INTO users(user_id) VALUES(?)", (user_id, ))
            self.connect.commit()

            self.user_counter += 1

            db_logger.info("New user added")
            db_logger.info(f"Users counter: {self.user_counter}")
