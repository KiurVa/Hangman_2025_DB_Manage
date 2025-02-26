import os
import sqlite3


class Database:
    db_name = os.path.join('databases', 'hangman_2025.db') #Andmebaasi asukoht databases/hangman_2025.db

    def __init__(self):
        self.conn = None
        self.cursor = None
        self.connect()
        self.check_tables()

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
            self.create_words_table()

    def create_words_table(self):
        words = """
                CREATE TABLE words (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    word TEXT NOT NULL,
                    category TEXT NOT NULL
                );
                """
        self.cursor.execute(words)
        self.conn.commit()
        print('Tabel words on loodud.')

    def get_unique_categories(self):
        """Leiab words tabelist kõik unikaalsed kategooriad ja lisab esimeseks 'Vali Kategooria'"""
        self.cursor.execute('SELECT DISTINCT category FROM words;')
        categories = [row[0] for row in self.cursor.fetchall()]
        categories.sort()
        categories.insert(0, 'Vali kategooria')
        return [category.capitalize() for category in categories]

    def read_words(self):
        """Loeb wordsi tabelist andmed ja tagastab data"""
        try:
            self.cursor.execute('SELECT COUNT(*) FROM words;')  # Kontrollib, kas tabelis on mingeid ridu
            count = self.cursor.fetchone()[0]
            if count == 0:
                return []  # Kui ridu ei ole, tagastab tühi loend
            self.cursor.execute('SELECT * FROM words ORDER BY category, word;')
            data = self.cursor.fetchall()
            return data
        except Exception as e:
            print(f"Error reading leaderboard: {e}")
            return []

    def add_word(self, word, category):
        """Lisab sõna tabelisse words"""
        try:
            if not word or not category: #Veendume, et midagi oleks sisestatud
                raise ValueError('Sisestage nii sõna kui ka kategooria')
            """Lisame sõna ja kategooria tabelisse"""
            self.cursor.execute('INSERT INTO words (word, category) VALUES (?, ?)', (word, category))
            self.conn.commit()
            print(f'Sõna {word} on lisatud kategooriasse {category}')
        except sqlite3.Error as e:
            print(f'Viga sõna lisamisel tabelisse {e}')
        except ValueError as e:
            print(f'Viga: {e}')


