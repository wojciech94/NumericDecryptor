from tkinter import Tk, Frame, Button, Label, Entry, StringVar, font
from pinDecryptor import PinDecryptor


class Appwindow(Tk):

    def __init__(self):
        super().__init__()
        self.geometry('{0}x{1}'.format(self.winfo_screenwidth(), self.winfo_screenheight()-100))
        self.title('Numeric Decryptor')

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.rowconfigure(0, weight=1)

        self.menu_frame = None
        self.active_frame = None
        self.font = None
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
            for l in elements:
                l.destroy()
            self.active_frame = None

    def init_font(self):
        self.font = font.Font(family='courier', size=16, weight='bold')

    def init_menu(self):
        if self.menu_frame is None:
            self.menu_frame = Frame(self, background='#56809C')
            self.menu_frame.columnconfigure(0, weight=1, uniform=1)
            for i in range(6):
                self.menu_frame.rowconfigure(i, weight=1, uniform=1)
            self.menu_frame.rowconfigure(6, weight=4, uniform=1)
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
        b_show_database_users = Button(self.menu_frame, font=self.font, bg='#394B59', fg='white',
                                       text='Show users database', command=lambda: self.show_database_frame())
        b_show_database_users.grid(column=0, row=2, padx=5, pady=5, sticky='nsew')
        b_encrypt_cypher = Button(self.menu_frame, font=self.font, bg='#394B59', fg='white', text='Encrypt cypher',
                                  command=lambda: self.encrypt_cypher_frame())
        b_encrypt_cypher.grid(column=0, row=3, padx=5, sticky='nsew')
        b_decrypt_cypher = Button(self.menu_frame, font=self.font, bg='#394B59', fg='white', text='Decrypt cypher',
                                  command=lambda: self.decrypt_cypher_frame())
        b_decrypt_cypher.grid(column=0, row=4, padx=5, pady=5, sticky='nsew')
        b_show_options = Button(self.menu_frame, font=self.font, bg='#394B59', fg='white', text='Show help',
                                command=lambda: self.show_help_frame())
        b_show_options.grid(column=0, row=5, padx=5, sticky='nsew')

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
            show_id_frame.grid(column=0, row=6, padx=5, pady=5, sticky='nsew')
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

    def add_user(self):
        self.clear_elements()

    def delete_user(self):
        self.clear_elements()

    def manage_users_frame(self):
        self.clear_elements()

    def show_database_frame(self):
        self.clear_elements()

    def encrypt_cypher_frame(self):
        self.clear_elements()

    def decrypt_cypher_frame(self):
        self.clear_elements()

    def show_help_frame(self):
        self.clear_elements()
