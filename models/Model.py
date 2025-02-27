from models.Database import Database


class Model:
    def __init__(self):
        self.__database = Database()
        self.__categories = self.__database.get_unique_categories()
        self.__data = self.__database.read_words()
        self.word_id = None

    def read_words(self):
        """kasutab Database read_words ja saaks seda välja kutsuda View.py"""
        return self.__database.read_words()

    def add_word(self, word, category):
        self.__database.add_word(word, category)

    def edit_word_category(self, word, category, item_id):
        self.__database.edit_word_category(word, category, item_id)

    def delete_word(self,word, category,  item_id):
        self.__database.delete_word(word, category, item_id)

    def refresh_categories(self):
        """Comboboxi uuendamiseks uued kategooriad"""
        self.__categories = self.__database.get_unique_categories()

    #GETTERS
    @property
    def categories(self): #tagastab kategooriate listi
        return self.__categories

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, data):
        self.__data = data

