from tkinter import END


class Controller:
    def __init__(self, model, view):
        """
        Kontrolleri konstruktor
        :param model: main-is loodud mudel
        :param view:  main-is loodud view
        """
        self.model = model
        self.view = view

        # Rippmenüü funktsionaalsus
        self.view.get_combo_categories.bind("<<ComboboxSelected>>", self.combobox_change)

        #Nuppude callback seaded
        self.btn_add_callback()

    def combobox_change(self, event=None):
        """
        Kui valitakse rippmenüüst tegevus, saadakse kätte tekst kui ka index (print lause). Näide kuidas võiks
        rippmenüü antud rakenduses töötada :)
        :param event: vaikimisi pole
        :return: None
        """
        # print(self.view.get_combo_categories.get(), end=" => ") # Tekst rippmenüüst => Hoonaed
        # print(self.view.get_combo_categories.current()) # Rippmenüü index => 1
        if self.view.get_combo_categories.current() > 0:  # Vali kategooria on 0
            self.view.get_txt_category.delete(0, END) # Tühjenda uue kategooria sisestuskast
            self.view.get_txt_category.config(state='disabled')  # Ei saa sisestada uut kategooriat
            self.view.get_txt_word.focus()
        else:
            self.view.get_txt_category.config(state='normal')  # Saab sisestada uue kategooria
            self.view.get_txt_category.focus()

    def btn_add_callback(self):
        self.view.set_button_new_callback(self.btn_add_click)

    def btn_add_click(self):
        word = self.view.get_txt_word.get()
        category = self.view.get_combo_categories.get()

        if category == 'Vali Kategooria':
            category = self.view.get_txt_category.get()

        if word and category:
            self.model.add_word(word, category)
            self.view.get_txt_word.delete(0, END)
            self.view.get_txt_category.delete(0, END)
            self.view.get_combo_categories.current(0)
            self.view.get_txt_word.focus()
            self.view.vsb.destroy()
            self.view.get_my_table.destroy()
            self.model.data = self.model.read_words()
            self.view.create_table()
        else:
            print('Palun täitke kõik vajalikud väljad.')