from tkinter import *
from tkinter.ttk import Combobox, Treeview


class View(Tk):

    def __init__(self, model):
        """
        Põhi akna konstruktor
        """
        super().__init__() # Pärib kõik originaal Tk omadused: View(Tk)
        self.model = model
        self.__myTable = None
        self.vsb = None
        self.word_id = None
        self.combo = None

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        # Põhiaken
        self.__width = 400
        self.__height = 300
        self.title('Poomismängu andmebaasi haldus')
        self.center(self, self.__width, self.__height)

        # Paneel
        self.__frame_top, self.__frame_bottom, self.__frame_right = self.create_frames()

        # Põhivorm
        self.__lbl_category, self.__txt_category, self.__lbl_word, self.__txt_word = self.create_main_form()

        # Vana kategooria valik
        self.__lbl_old_categories, self.__combo_categories = self.create_combobox()

        # Nupud
        self.__btn_add, self.__btn_edit, self.__btn_delete = self.create_buttons()

        self.create_table()

    @staticmethod
    def center(win, w, h):
        """
        Meetod mis paigutab etteantud akna ekraani keskele vastavalt monitori suurusele
        :param win: aken mida paigutada
        :param w:   akna laius
        :param h:   akna kõrgus
        :return:    None
        """
        x = int((win.winfo_screenwidth() / 2) - (w / 2))
        y = int((win.winfo_screenheight() / 2) - (h / 2))
        win.geometry(f'{w}x{h}+{x}+{y}')

    def create_frames(self):
        """
        Loob kaks frame mis paigutatakse põhiaknale (View)
        :return:
        """
        top = Frame(self, height=50, background='lightblue')
        bottom = Frame(self, background='lightyellow')
        right = Frame(top, background='lightgray')

        # Paneme paneelid põhi aknale
        top.pack(fill=BOTH)
        bottom.pack(fill=BOTH, expand=True)
        right.grid(row=0, column=2, rowspan=2, padx=5, pady=5)

        return top, bottom, right # Tagastame loodud paneelid õiges järjekorras

    def create_main_form(self):
        """
        Loob põhi vormi kaks labelit ja kaks sisestuskasti
        :return: lbl_1, txt_1, lbl_2, txt_2
        """
        lbl_1 = Label(self.__frame_top, text='Uus kategooria:', background='lightblue', font=('Verdana', 10, 'bold'))
        txt_1 = Entry(self.__frame_top)
        txt_1.focus()
        lbl_1.grid(row=0, column=0, pady=5, sticky=EW)
        txt_1.grid(row=0, column=1, sticky=EW)

        lbl_2 = Label(self.__frame_top, text='Sõna:', background='lightblue', font=('Verdana', 10, 'bold'))
        lbl_2.grid(row=2, column=0, pady=5, sticky=EW)
        txt_2 = Entry(self.__frame_top)
        txt_2.grid(row=2, column=1, sticky=EW)

        return lbl_1, txt_1, lbl_2, txt_2

    def create_buttons(self):
        """
        Loob kolm nuppu CRUD jaoks. Antud juhul: CUD (Create, Update, Delete)
        :return: btn_1, btn_2, btn_3
        """
        btn_add = Button(self.__frame_right, text='Lisa')
        btn_edit = Button(self.__frame_right, text='Muuda')
        btn_delete = Button(self.__frame_right, text='Kustuta')

        btn_add.grid(row=0, column=1, padx=1, sticky=EW)
        btn_edit.grid(row=1, column=2, padx=1, sticky=EW)
        btn_delete.grid(row=0, column=2, padx=1, sticky=EW)

        return btn_add, btn_edit, btn_delete

    def create_combobox(self):
        """
        Loob ja tagastab rippmenüü labeli ja rippmenüü enda
        :return: label, combo
        """
        label = Label(self.__frame_top, text='Vana kategooria', background='lightblue', font=('Verdana', 10, 'bold'))
        label.grid(row=1, column=0, pady=5, sticky=EW)

        self.combo = Combobox(self.__frame_top)
        self.combo['values'] = self.model.categories # Näidis
        self.combo.current(0)
        self.combo.grid(row=1, column=1, padx=4, sticky=EW)

        return label, self.combo

    def create_table(self):
        """
        Loob tabeli mis näitab kirjeid (sõnu ja nende kategooriaid). Loodud ainult tabeli päise osa
        :return: None
        """
        self.__myTable = None
        self.__myTable = Treeview(self.__frame_bottom)

        self.vsb = Scrollbar(self.__frame_bottom, orient=VERTICAL, command=self.__myTable.yview)
        self.vsb.pack(side=RIGHT, fill=Y)
        self.__myTable.configure(yscrollcommand=self.vsb.set)

        self.__myTable['columns'] = ('jrk', 'id', 'word', 'category')

        self.__myTable.column('#0', width=0, stretch=NO)
        self.__myTable.column('jrk', anchor=W, width=25)
        self.__myTable.column('id', anchor=W, width=50)
        self.__myTable.column('word', anchor=W, width=100)
        self.__myTable.column('category', anchor=W, width=100)

        self.__myTable.heading('#0', text='', anchor=CENTER)
        self.__myTable.heading('jrk', text='Jrk', anchor=CENTER)
        self.__myTable.heading('id', text='ID', anchor=CENTER)
        self.__myTable.heading('word', text='Sõna', anchor=CENTER)
        self.__myTable.heading('category', text='Kategooria', anchor=CENTER)

        # (START) Siin peaks olema andmete tabelisse lisamise või uuendamise koht

        x = 0
        for word in self.model.data:
            self.__myTable.insert(parent='', index='end', iid=str(x), text='',
                                 values=(x+1, word[0], word[1], word[2],))
            x += 1
        # (LÕPP) Siin peaks olema andmete tabelisse lisamise või uuendamise koht
        self.__myTable.pack(fill=BOTH, expand=True)

        self.__myTable.bind('<Double-1>', self.on_row_double_click) #Topelt kliki sündmus


    def set_button_new_callback(self, callback):
        """Kui vajutatakse lisa nuppu"""
        self.__btn_add.config(command=callback)

    def set_button_edit_callback(self, callback):
        """Kui vajutatakse muuda nuppu"""
        self.__btn_edit.config(command=callback)

    def set_button_delete_callback(self, callback):
        """Kui vajutatakse kustuta nuppu"""
        self.__btn_delete.config(command=callback)

    def on_row_double_click(self, event):
        """Topeltkliki väärtuste saamine ja panemine lahtritesse"""
        selected_item = self.__myTable.selection()
        if selected_item:
            row_values = self.__myTable.item(selected_item, 'values')
            word = row_values[2]
            category = row_values[3]
            self.model.word_id = row_values[1]

            self.__txt_word.delete(0, END)
            self.__txt_word.insert(0, word)
            self.__combo_categories.set(category) #Vali kategooria asemele ilmub valitud kategooria
            self.__txt_category['state'] = DISABLED #Muudab kategooria mitteaktiivseks
            #self.get_txt_category.delete(0, END)
            #self.get_txt_category.insert(0, category)
            print(self.model.word_id)

    def update_combobox(self):
        """Värskendab rippmenüü sisu vastavalt"""
        self.__combo_categories['values'] = self.model.categories
        self.__combo_categories.current(0)





    # GETTERS

    @property
    def get_combo_categories(self):
        """
        Tagastab rippmenüü objekti
        :return: Combobox
        """
        return self.__combo_categories

    @property
    def get_txt_category(self):
        """
        Tagastab uue kategooria sisestuskasti objekti
        :return: Entry objekt
        """
        return self.__txt_category

    @property
    def get_my_table(self):
        """
        Meetod on selleks et saaks tabeli objekti mujal kasutada
        :return: tagastab __myTable objekti
        """
        return self.__myTable

    @property
    def get_txt_word(self):
        """
        Tagastab sisestuskasti kuhu saab sisestada sõna
        :return: Entry objekt
        """
        return self.__txt_word