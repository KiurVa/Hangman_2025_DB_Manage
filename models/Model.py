class Model:
    def __init__(self, db):
        self.__database = db
        self.__categories = self.__database.get_unique_categories()

    #GETTERS
    @property
    def categories(self): #tagastab kategooriate listi
        return self.__categories

    def read_words(self):
        """kasutab Database read_words ja saaks seda välja kutsuda View.py"""
        return self.__database.read_words()