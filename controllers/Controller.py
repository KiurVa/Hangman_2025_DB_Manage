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
        self.btn_edit_callback()
        self.btn_delete_callback()

    def combobox_change(self, event=None):
        """
        Kui valitakse rippmenüüst tegevus, saadakse kätte tekst kui ka index (print lause). Näide kuidas võiks
        rippmenüü antud rakenduses töötada :)
        :param event: vaikimisi pole
        :return: None
        """
        #print(self.view.get_combo_categories.get(), end=" => ") # Tekst rippmenüüst => Hoonaed
        #print(self.view.get_combo_categories.current()) # Rippmenüü index => 1
        if self.view.get_combo_categories.current() > 0:  # Vali kategooria on 0
            self.view.get_txt_category.delete(0, END)  # Tühjenda uue kategooria sisestuskast
            self.view.get_txt_category.config(state='disabled')  # Ei saa sisestada uut kategooriat
            self.view.get_txt_word.focus()
        else:
            self.view.get_txt_category.config(state='normal')  # Saab sisestada uue kategooria
            self.view.get_txt_category.focus()

    def btn_add_callback(self):
        self.view.set_button_new_callback(self.btn_add_click)

    def btn_edit_callback(self):
        self.view.set_button_edit_callback(self.btn_edit_click)

    def btn_delete_callback(self):
        self.view.set_button_delete_callback(self.btn_delete_click)

    def btn_add_click(self):
        """lisa nuppu toimime"""
        word = self.view.get_txt_word.get().lower().strip()
        category = self.view.get_combo_categories.get().lower().strip() #Võtab kategooria rippmenüüst

        if self.view.get_combo_categories.current() == 0: #Kategooria on vali kategooria, siis loeb teksti lahtrist
            category = self.view.get_txt_category.get().lower().strip()

        if word and category:
            self.model.add_word(word, category) #Lisab uue sõna andmebaasi
            self.view.get_txt_word.delete(0, END)
            self.view.get_txt_category.delete(0, END)
            self.view.get_combo_categories.current(0)
            self.view.get_txt_word.focus() #Teeb kastid tühjaks jne
            self.view.vsb.destroy() #Hävitab kerimise
            self.view.get_my_table.destroy() #Hävitab my table
            self.model.data = self.model.read_words() #Võtab uue data uuendatud.
            self.view.create_table() #Teeb tabeli uuesti
        else:
            print('Palun täitke kõik vajalikud väljad.')

    def btn_edit_click(self):
        """Muuda nupu toimime"""
        word = self.view.get_txt_word.get().lower().strip()
        category = self.view.get_combo_categories.get().lower().strip()
        item_id = self.model.word_id

        if self.view.get_combo_categories.current() == 0: #Kategooria on vali kategooria, siis loeb teksti lahtrist
            category = self.view.get_txt_category.get().lower().strip()

        if word and category:
            self.model.edit_word_category(word, category, item_id)
            self.view.get_txt_word.delete(0, END)
            self.view.get_txt_category.delete(0, END)
            self.view.get_combo_categories.current(0)
            self.view.get_txt_word.focus()  # Teeb kastid tühjaks jne
            self.view.vsb.destroy()  # Hävitab kerimise
            self.view.get_my_table.destroy()  # Hävitab my table
            self.model.data = self.model.read_words()  # Võtab uue data uuendatud.
            self.view.create_table()  # Teeb tabeli uuesti
        else:
            print('Palun täitke kõik vajalikud väljad.')

    def btn_delete_click(self):
        word = self.view.get_txt_word.get().strip()
        category = self.view.get_combo_categories.get().strip()
        item_id = self.model.word_id

        if self.view.get_combo_categories.current() == 0: #Kategooria on vali kategooria, siis loeb teksti lahtrist
            category = self.view.get_txt_category.get().lower().strip()

        if word and category:
            self.model.delete_word(word, category, item_id)
            self.view.get_txt_word.delete(0, END)
            self.view.get_txt_category.delete(0, END)
            self.view.get_combo_categories.current(0)
            self.view.get_txt_word.focus()  # Teeb kastid tühjaks jne
            self.view.vsb.destroy()  # Hävitab kerimise
            self.view.get_my_table.destroy()  # Hävitab my table
            self.model.data = self.model.read_words()  # Võtab uue data uuendatud.
            self.view.create_table()  # Teeb tabeli uuesti
        else:
            print('Palun täitke kõik vajalikud väljad.')
