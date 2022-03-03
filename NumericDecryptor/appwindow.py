from tkinter import Tk, Frame, Button, Label, Entry, StringVar, PhotoImage, font
from pinDecryptor import PinDecryptor


class Appwindow(Tk):

    def __init__(self):
        super().__init__()
        self.geometry('{0}x{1}'.format(self.winfo_screenwidth(), self.winfo_screenheight() - 100))
        self.title('Numeric Decryptor')

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.rowconfigure(0, weight=1)

        self.menu_frame = None
        self.active_frame = None
        self.font = None
        self.rem_img = None
        self.add_img = None
        self.debug_info = StringVar()
        self.public_key_label = StringVar()
        self.cypher_range_label = StringVar()
        self.cypher_entry = StringVar()
        self.pin_decryptor = PinDecryptor()
        self.init_font()
        self.init_menu()
        self.show_menu_frame()
        self.show_id_frame()

    def clear_elements(self):
        if self.active_frame is not None:
            elements = self.active_frame.grid_slaves()
            for el in elements:
                el.destroy()
            self.active_frame = None

    def init_font(self):
        self.font = font.Font(family='courier', size=16, weight='bold')

    def init_menu(self):
        if self.menu_frame is None:
            self.menu_frame = Frame(self, background='#56809C')
            self.menu_frame.columnconfigure(0, weight=1, uniform='1')
            for i in range(5):
                self.menu_frame.rowconfigure(i, weight=1, uniform='1')
            self.menu_frame.rowconfigure(5, weight=3, uniform='1')
            self.menu_frame.grid(column=0, row=0, rowspan=5, sticky='nsew')
            self.menu_frame.grid_propagate(False)
            self.cypher_range_label.set(str(self.pin_decryptor.cypher_range))
            self.public_key_label.set(str(self.pin_decryptor.public_key))

    def show_menu_frame(self):
        b_create_id = Button(self.menu_frame, font=self.font, bg='#394B59', fg='white',
                             text='Create your identyficator', command=lambda: self.create_id_frame())
        b_create_id.grid(column=0, row=0, padx=5, pady=5, sticky='nsew')
        b_manage_users = Button(self.menu_frame, font=self.font, bg='#394B59', fg='white', text='Manage users',
                                command=lambda: self.manage_users_frame())
        b_manage_users.grid(column=0, row=1, padx=5, sticky='nsew')
        b_encrypt_cypher = Button(self.menu_frame, font=self.font, bg='#394B59', fg='white', text='Encrypt cypher',
                                  command=lambda: self.encrypt_cypher_frame())
        b_encrypt_cypher.grid(column=0, row=2, padx=5, pady=5, sticky='nsew')
        b_decrypt_cypher = Button(self.menu_frame, font=self.font, bg='#394B59', fg='white', text='Decrypt cypher',
                                  command=lambda: self.decrypt_cypher_frame())
        b_decrypt_cypher.grid(column=0, row=3, padx=5, sticky='nsew')
        b_show_options = Button(self.menu_frame, font=self.font, bg='#394B59', fg='white', text='Show help',
                                command=lambda: self.show_help_frame())
        b_show_options.grid(column=0, row=4, padx=5, pady=5, sticky='nsew')

    def create_id_frame(self):
        self.clear_elements()
        self.update_cypher_entry()
        create_id_frame = Frame(self, background='#D9DCFB')
        create_id_frame.grid(column=1, row=0, sticky='nsew')
        for c in range(2):
            create_id_frame.columnconfigure(c, weight=1, uniform='1')
        for r in range(4):
            create_id_frame.rowconfigure(r, weight=1, uniform='1')
        create_id_frame.grid_propagate(False)
        pub_key_txt = StringVar(create_id_frame, 'Public Key:')
        prv_key_txt = StringVar(create_id_frame, 'Private Key:')
        self.cypher_entry.trace('w', self.update_cypher_entry)
        entry_font = font.Font(family='courier', size=16, slant='italic')
        l0 = Label(create_id_frame, bg='#394B59', fg='red', font=self.font, textvariable=self.debug_info)
        l0.grid(column=0, columnspan=2, row=0, padx=5, pady=5, sticky='nsew')
        l1 = Label(create_id_frame, bg='#394B59', fg='white', text='Cypher range', font=self.font)
        l1.grid(column=0, row=1, padx=5, pady=5, sticky='nsew')
        e1 = Entry(create_id_frame, bg='#394B59', fg='white', textvariable=self.cypher_entry, font=entry_font,
                   justify='center')
        e1.grid(column=1, row=1, padx=5, pady=5, sticky='nsew')
        b1 = Button(create_id_frame, bg='#394B59', fg='white', text='Generate Identyficator', font=self.font,
                    command=lambda: self.gen_identity(pub_key_txt, prv_key_txt))
        b1.grid(column=0, row=2, columnspan=2, padx=5, pady=5, sticky='nsew')
        l2 = Label(create_id_frame, bg='#394B59', fg='white', textvariable=pub_key_txt, font=self.font)
        l2.grid(column=0, row=3, padx=5, pady=5, sticky='nsew')
        l3 = Label(create_id_frame, bg='#394B59', fg='white', textvariable=prv_key_txt, font=self.font)
        l3.grid(column=1, row=3, padx=5, pady=5, sticky='nsew')
        self.active_frame = create_id_frame

    def gen_identity(self, pub_key, prv_key):
        if self.debug_info.get() == '' and len(self.cypher_entry.get()) > 0:
            generated_keys = self.pin_decryptor.generate_identity(self.cypher_entry.get())
            if len(generated_keys) == 3:
                pub_key.set('Public Key:{0}'.format(generated_keys[0]))
                prv_key.set('Private Key:{0}'.format(generated_keys[1]))
                self.public_key_label.set(str(generated_keys[0]))
                self.cypher_range_label.set(str(generated_keys[2]))

    def update_cypher_entry(self, *args):
        if len(self.cypher_entry.get()) == 0:
            self.debug_info.set('Type Cypher range in the row below')
        elif not self.cypher_entry.get().isnumeric():
            self.debug_info.set('Cypher is not numeric value')
        elif len(self.cypher_entry.get()) > 5:
            self.debug_info.set('Cypher range is too large to compute')
        else:
            self.debug_info.set('')

    def show_id_frame(self):
        if self.menu_frame is not None:
            show_id_frame = Frame(self.menu_frame, bg='#394B59')
            show_id_frame.grid(column=0, row=5, padx=5, pady=5, sticky='nsew')
            show_id_frame.grid_propagate(False)
            show_id_frame.columnconfigure(0, weight=1)
            for i in range(4):
                show_id_frame.rowconfigure(i, weight=1, uniform='1')
            label1 = Label(show_id_frame, height=2, bg='#56809C', fg='white', text='Your identyficator', font=self.font)
            label1.grid(column=0, row=0, padx=5, sticky='ew')
            label2 = Label(show_id_frame, height=2, bg='#56809C', fg='white', textvariable=self.public_key_label,
                           font=self.font)
            label2.grid(column=0, row=1, padx=5, sticky='ew')
            label3 = Label(show_id_frame, height=2, bg='#56809C', fg='white', text='Cypher Range', font=self.font)
            label3.grid(column=0, row=2, padx=5, pady=5, sticky='ew')
            label4 = Label(show_id_frame, height=2, bg='#56809C', fg='white', textvariable=self.cypher_range_label,
                           font=self.font)
            label4.grid(column=0, row=3, padx=5, sticky='ew')

    def manage_users_frame(self):
        self.clear_elements()
        self.rem_img = PhotoImage(file='delete.png')
        self.add_img = PhotoImage(file='add.png')
        show_db_frame = Frame(self, background='#D9DCFB')
        show_db_frame.grid(column=1, row=0, sticky='nsew')
        txtsample = self.get_db_users()
        rows = len(txtsample)
        for i in range(5):
            show_db_frame.columnconfigure(i, weight=1, uniform='1')
        for j in range(len(txtsample) + 5):
            show_db_frame.rowconfigure(j, weight=1, uniform='1')
        show_db_frame.grid_propagate(False)
        lb1 = Label(show_db_frame, bg='#D9DCFB', font=self.font, text='List of users')
        lb1.grid(column=0, columnspan=4, row=0, sticky='nsew')
        titlab = ['Id', 'Nick', 'Public Key', 'Range']
        lab = [['' for x in range(4)] for y in range(rows)]
        butt = [['' for x in range(4)] for y in range(rows)]
        add_ent = ['' for x in range(4)]
        for i in range(4):
            Label(show_db_frame, text=titlab[i], font=self.font, justify='center').grid(
                column=i, row=1, sticky='nsew', padx=5, pady=5)
            Label(show_db_frame, text=titlab[i], font=self.font, justify='center').grid(
                column=i, row=len(txtsample) + 3, sticky='nsew', padx=5, pady=5)
        for j in range(rows):
            for k in range(4):
                lab[j][k] = Label(show_db_frame, text=txtsample[j][k], font=self.font, justify='center')
                lab[j][k].grid(column=k, row=j + 2, sticky='nsew', padx=5, pady=5)
            butt[j] = Button(show_db_frame, image=self.rem_img, bg='#C9CCCB', borderwidth=0, activebackground='#C9CCCB',
                             command=lambda jj=j: self.delete_user(txtsample[jj][0]))
            butt[j].grid(column=4, row=j + 2, padx=5, pady=5)
        lb2 = Label(show_db_frame, bg='#D9DCFB', font=self.font, text='Add User to Database')
        lb2.grid(column=0, columnspan=4, row=len(txtsample) + 2, sticky='nsew')
        ent_txt_var = [StringVar(show_db_frame) for i in range(4)]
        for i in range(4):
            add_ent[i] = Entry(show_db_frame, font=self.font, justify='center',
                               textvariable=ent_txt_var[i])
            add_ent[i].grid(column=i, row=len(txtsample) + 4, sticky='nsew', padx=5, pady=5)
        abutt = Button(show_db_frame, image=self.add_img, bg='#C9CCCB', borderwidth=0, activebackground='#C9CCCB',
                       command=lambda: self.add_user(ent_txt_var))
        abutt.grid(column=4, row=len(txtsample) + 4, padx=5, pady=5)
        self.active_frame = show_db_frame

    def get_db_users(self):
        data = self.pin_decryptor.databasemanager.get_all()
        data = [d for d in data]
        return data

    def add_user(self, user_pack):
        if len(user_pack) == 4:
            self.pin_decryptor.add_user(user_pack[0].get(), user_pack[1].get(), user_pack[2].get(), user_pack[3].get())
        self.show_database_frame()

    def delete_user(self, uid):
        self.pin_decryptor.delete_user(uid)
        self.show_database_frame()

    def encrypt_cypher_frame(self):
        pass

    def decrypt_cypher_frame(self):
        self.clear_elements()

    def show_help_frame(self):
        self.clear_elements()
