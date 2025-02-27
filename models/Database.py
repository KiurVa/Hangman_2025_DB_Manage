import os
import sqlite3


class Database:
    db_directory = 'databases'
    db_name = os.path.join(db_directory, 'hangman_2025.db') #Andmebaasi asukoht databases/hangman_2025.db

    def __init__(self):
        self.conn = None
        self.cursor = None
        self.check_database()
        self.connect()
        self.check_tables()

    def check_database(self):
        """Kontrollib kas databases kaust olemas ja kas seal on fail hangman_2025.db"""
        if not os.path.exists(self.db_directory):
            os.makedirs(self.db_directory)
            print(f'Kaust {self.db_directory} on loodud.')
        if not os.path.exists(self.db_name):
            self.create_database()

    def create_database(self):
        """Loob andmebaasi faili ja tühja words tabeli"""
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            print(f'Andmebaas {self.db_name} on loodud.')
            print(f'Ühendus andmebaasiga {self.db_name} on loodud.')
            self.create_words_table()
        except sqlite3.Error as e:
            print(f'Tõrge andmebaasi loomisel: {e}')
        finally:
            if self.conn:
                self.conn.close()
                print(f'Ühendus andmebaasiga {self.db_name} suletud.')
                self.conn = None
                self.cursor = None

    def check_tables(self):
        """Kontrollib words tabeli olemasolu"""
        self.cursor.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="words";')
        if not self.cursor.fetchone():
            self.create_words_table()
        else:
            self.cursor.execute('PRAGMA table_info(words);')
            columns = {row[1] for row in self.cursor.fetchall()}
            required_columns = {'id', 'word', 'category'}

            if columns != required_columns:
                print("Tabel words struktuur ei ole korrektne. Teen uue tabeli words ja vana nimetan ümber words_old.")
                self.cursor.execute('ALTER TABLE words RENAME TO words_old;')
                self.create_words_table()
                self.conn.commit()

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


    def connect(self):
        """Loob ühenduse andmebaasiga"""
        try:
            if self.conn:
                self.conn.close()  # Kui ühendus, siis sulgeks
                print('Varasem ühendus suleti.')
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            print(f'Ühendus andmebaasiga {self.db_name} on loodud.')
        except sqlite3.Error as e:
            print(f'Tõrge andmebaasi ühenduse loomisel: {e}')
            self.conn = None
            self.cursor = None

    def close_connection(self):
        """Sulgeb andmebaasi ühenduse"""
        try:
            if self.conn:
                self.conn.close()
                print(f'Ühendus andmebaasiga {self.db_name} suletud.')
                self.conn = None
                self.cursor = None
        except sqlite3.Error as error:
            print(f'Tõrge ühenduse sulgemisel: {error}')


    def get_unique_categories(self):
        """Leiab words tabelist kõik unikaalsed kategooriad ja lisab esimeseks 'Vali Kategooria'"""
        if self.cursor:
            try:
                self.cursor.execute('SELECT DISTINCT category FROM words;')
                categories = [row[0] for row in self.cursor.fetchall()]
                categories.sort()
                categories.insert(0, 'Vali kategooria')
                return [category.capitalize() for category in categories]
            except sqlite3.Error as e:
                print(f'Unikaalsete kategooriate lugemisel tekkis tõrge {e}.')
        else:
            print('Ühendus andmebaasiga puudub. Palun loo ühendus andmebaasiga.')


    def read_words(self):
        """Loeb wordsi tabelist andmed ja tagastab data"""
        if self.cursor:
            try:
                self.cursor.execute('SELECT COUNT(*) FROM words;')  # Kontrollib, kas tabelis on mingeid ridu
                count = self.cursor.fetchone()[0]
                if count == 0:
                    return []  # Kui ridu ei ole, tagastab tühi loend
                self.cursor.execute('SELECT * FROM words ORDER BY category, word;')
                data = self.cursor.fetchall()
                return data
            except Exception as e:
                print(f"Tabeli lugemisel tekkis tõrge: {e}")
                return []
            finally:
                self.close_connection()

    def add_word(self, word, category):
        """Lisab sõna tabelisse words"""
        self.connect()
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

    def edit_word_category(self, word, category, item_id):
        """Sõna või kategooria muutmine"""
        self.connect()
        try:
            self.cursor.execute('UPDATE words SET word=?, category=? WHERE id=?', (word, category, item_id))
            self.conn.commit()
            print(f'Sõna {word} on muudetud kategoorias {category}.')
        except sqlite3.Error as e:
            print(f'Viga kirje muutmisel: {e}.')

    def delete_word(self,word, category, item_id):
        """valitud sõna kustutamine andmebaasist"""
        self.connect()
        try:
            self.cursor.execute('DELETE FROM words WHERE id=?', (item_id,))
            self.conn.commit()
            print(f'Sõna {word} on kustutatud kategooriast {category}.')
        except sqlite3.Error as e:
            print(f'Viga kirje kustutamisel: {e}.')
