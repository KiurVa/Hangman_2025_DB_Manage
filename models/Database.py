import os
import sqlite3


class Database:

    def __init__(self):
        self.conn = None
        self.cursor = None
        self.connect()

    def connect(self):
        """Loob ühenduse andmebaasiga ja kontrollib, kas andmebaas on olemas"""
        if not os.path.exists(self.db_name):
            raise FileNotFoundError('Andmebaasi ei ole. Rakendus ei käivitu.')
        try:
            if self.conn:
                self.conn.close()  # Kui ühendus, siis sulgeks
                print('Varasem ühendus suleti.')
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            print(f'Ühendus andmebaasiga {self.db_name} on loodud.')
        except sqlite3.Error as e:
            raise Exception(f'Tõrge andmebaasi ühenduse loomisel: {e}')

    def check_tables(self):
        """Kontrollib words tabeli olemasolu"""
        self.cursor.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="words";')
        if not self.cursor.fetchone():
            raise FileNotFoundError('Tabel words puudub. Rakendus ei käivitu.')
        """Kontrollib, kas words tabelis on sõnu ja kategooriad"""
        self.cursor.execute('SELECT * FROM words;')
        if not self.cursor.fetchone():
            raise ValueError('Tabel words on tühi. Rakendus ei käivitu.')
        """Kontrollib kas leaderboard tabel on olemas ja vajadusel käivitab selle tegemise"""
        self.cursor.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="leaderboard";')
        if not self.cursor.fetchone():
            self.create_leaderboard_table()
