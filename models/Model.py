class Model:
    def __init__(self, db):
        self.__database = db
        self.__categories = self.__database.get_unique_categories()
        self.__data = self.__database.read_words()

    def read_words(self):
        """kasutab Database read_words ja saaks seda välja kutsuda View.py"""
        return self.__database.read_words()

    def add_word(self, word, category):
        self.__database.add_word(word, category)

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

