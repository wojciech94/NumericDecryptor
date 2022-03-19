from tkinter import Tk, Frame, Button, Label, Entry, StringVar, PhotoImage, font
from pinDecryptor import PinDecryptor, DecryptorMath


class Appwindow(Tk):

    def __init__(self):
        super().__init__()
        self.geometry('{0}x{1}'.format(self.winfo_screenwidth(), self.winfo_screenheight()))
        self.title('Numeric Decryptor')

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.rowconfigure(0, weight=1)

        self.full_state = True
        self.state('zoomed')
        self.bind("<Escape>", self.toggle_full_screen)

        self.menu_frame = None
        self.active_frame = None
        self.font = None
        self.mid_font = None
        self.rem_img = None
        self.add_img = None
        self.next_img = None
        self.prev_img = None
        self.help_mode = 1
        self.debug_info = StringVar()
        self.public_key_label = StringVar()
        self.cypher_range_label = StringVar()
        self.help_text = StringVar()
        self.pin_decryptor = PinDecryptor()
        self.init_font()
        self.init_img()
        self.init_menu()
        self.show_menu_frame()
        self.show_id_frame()
        self.show_help_frame()

    def clear_and_reset(self):
        self.clear_frame(self.active_frame)
        self.reset_state()

    def clear_frame(self, frame):
        if frame is not None:
            elements = frame.grid_slaves()
            for el in elements:
                el.destroy()

    def reset_state(self):
        self.debug_info.set('')
        self.help_mode = 1
        self.active_frame = None

    def toggle_full_screen(self, event=None):
        self.full_state = not self.full_state
        self.attributes('-fullscreen', self.full_state)

    def init_font(self):
        self.font = font.Font(family='courier', size=18, weight='bold')
        self.mid_font = font.Font(family='courier', size=22, weight='bold')

    def init_img(self):
        self.rem_img = PhotoImage(file='images/delete.png')
        self.add_img = PhotoImage(file='images/add.png')
        self.next_img = PhotoImage(file='images/next.png')
        self.prev_img = PhotoImage(file='images/prev.png')

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
                             text='Create your Id', command=lambda: self.create_id_frame())
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
        self.clear_and_reset()
        self.update_cypher_entry()
        create_id_frame = Frame(self, background='#394B59')
        create_id_frame.grid(column=1, row=0, sticky='nsew')
        for c in range(2):
            create_id_frame.columnconfigure(c, weight=1, uniform='1')
        for r in range(4):
            create_id_frame.rowconfigure(r, weight=1, uniform='1')
        create_id_frame.grid_propagate(False)
        pub_key_txt = StringVar(create_id_frame, 'Public Key:')
        prv_key_txt = StringVar(create_id_frame, 'Private Key:')
        cypher_entry_var = StringVar(create_id_frame)
        cypher_entry_var.trace('w', lambda *args: self.update_cypher_entry(cypher_entry_var))
        entry_font = font.Font(family='courier', size=20, slant='italic')
        l0 = Label(create_id_frame, bg='#D3D9FB', fg='red', font=self.mid_font, textvariable=self.debug_info)
        l0.grid(column=0, columnspan=2, row=0, padx=5, pady=5, sticky='nsew')
        l1 = Label(create_id_frame, bg='#D3D9FB', text='Cypher range', font=self.mid_font)
        l1.grid(column=0, row=1, padx=5, pady=5, sticky='nsew')
        e1 = Entry(create_id_frame, bg='#E3E9FF', textvariable=cypher_entry_var, font=entry_font,
                   justify='center')
        e1.grid(column=1, row=1, padx=5, pady=5, sticky='nsew')
        b1 = Button(create_id_frame, bg='#A8B2C8', text='Generate Id', font=self.mid_font,
                    command=lambda: self.gen_identity(pub_key_txt, prv_key_txt, cypher_entry_var))
        b1.grid(column=0, row=2, columnspan=2, padx=5, pady=5, sticky='nsew')
        l2 = Label(create_id_frame, bg='#D3D9FB', textvariable=pub_key_txt, font=self.mid_font)
        l2.grid(column=0, row=3, padx=5, pady=5, sticky='nsew')
        l3 = Label(create_id_frame, bg='#D3D9FB', textvariable=prv_key_txt, font=self.mid_font)
        l3.grid(column=1, row=3, padx=5, pady=5, sticky='nsew')
        self.active_frame = create_id_frame

    def gen_identity(self, pub_key, prv_key, cypher_entry):
        if self.debug_info.get() == '' and len(cypher_entry.get()) > 0:
            generated_keys = self.pin_decryptor.generate_identity(cypher_entry.get())
            if len(generated_keys) == 3:
                pub_key.set('Public Key:{0}'.format(generated_keys[0]))
                prv_key.set('Private Key:{0}'.format(generated_keys[1]))
                self.public_key_label.set(str(generated_keys[0]))
                self.cypher_range_label.set(str(generated_keys[2]))
                self.debug_info.set('Please save your private key securely\nYou will need it to decrypt messages')

    def update_cypher_entry(self, *args):
        if len(args) == 1:
            cypher_entry = args[0]
            if len(cypher_entry.get()) == 0:
                self.debug_info.set('Type Cypher range in the row below')
            elif not cypher_entry.get().isnumeric():
                self.debug_info.set('Cypher is not numeric value')
            elif len(cypher_entry.get()) > 5:
                self.debug_info.set('Cypher range is too large to compute')
            else:
                self.debug_info.set('')
        else:
            self.debug_info.set('Type Cypher range in the row below')

    def show_id_frame(self):
        if self.menu_frame is not None:
            show_id_frame = Frame(self.menu_frame, bg='#394B59')
            show_id_frame.grid(column=0, row=5, padx=5, pady=5, sticky='nsew')
            show_id_frame.grid_propagate(False)
            show_id_frame.columnconfigure(0, weight=1)
            for i in range(5):
                show_id_frame.rowconfigure(i, weight=1, uniform='1')
            label1 = Label(show_id_frame, height=2, bg='#56809C', fg='white', text='Your Id', font=self.font)
            label1.grid(column=0, row=0, padx=5, pady=5, sticky='ew')
            label2 = Label(show_id_frame, height=2, bg='#56809C', fg='white', text='Public Key', font=self.font)
            label2.grid(column=0, row=1, padx=5, sticky='ew')
            label3 = Label(show_id_frame, height=2, bg='#56809C', fg='white', textvariable=self.public_key_label,
                           font=self.font)
            label3.grid(column=0, row=2, padx=5, pady=5, sticky='ew')
            label4 = Label(show_id_frame, height=2, bg='#56809C', fg='white', text='Cypher Range', font=self.font)
            label4.grid(column=0, row=3, padx=5, sticky='ew')
            label5 = Label(show_id_frame, height=2, bg='#56809C', fg='white', textvariable=self.cypher_range_label,
                           font=self.font)
            label5.grid(column=0, row=4, padx=5, pady=5, sticky='ew')

    def manage_users_frame(self):
        self.clear_and_reset()
        show_db_frame = Frame(self, bg='#394B59')
        show_db_frame.grid(column=1, row=0, sticky='nsew')
        txtsample = self.get_db_users()
        rows = len(txtsample)
        for i in range(5):
            show_db_frame.columnconfigure(i, weight=1, uniform='1')
        for j in range(len(txtsample) + 5):
            show_db_frame.rowconfigure(j, weight=1, uniform='1')
        show_db_frame.grid_propagate(False)
        lb1 = Label(show_db_frame, bg='#A8B2C8', font=self.font, text='List of users')
        lb1.grid(column=0, columnspan=4, row=0, sticky='nsew', padx=5, pady=5)
        titlab = ['Id', 'Nick', 'Public Key', 'Range']
        lab = [[Label(show_db_frame, bg='#D3D9FB', font=self.font, justify='center') for _ in range(4)] for _ in range(rows)]
        butt = [Button(show_db_frame, image=self.rem_img, bg='#394B59', borderwidth=0, activebackground='#394B59')
                for _ in range(rows)]
        add_ent = [Entry(show_db_frame, font=self.font, justify='center') for _ in range(4)]
        for i in range(4):
            Label(show_db_frame, bg='#D3D9FB', text=titlab[i], font=self.font, justify='center').grid(
                column=i, row=1, sticky='nsew', padx=5, pady=5)
            Label(show_db_frame, bg='#D3D9FB', text=titlab[i], font=self.font, justify='center').grid(
                column=i, row=len(txtsample) + 3, sticky='nsew', padx=5, pady=5)
        for j in range(rows):
            for k in range(4):
                lab[j][k].configure(text=txtsample[j][k])
                lab[j][k].grid(column=k, row=j + 2, sticky='nsew', padx=5, pady=5)
            butt[j].configure(command=lambda jj=j: self.delete_user(txtsample[jj][0]))
            butt[j].grid(column=4, row=j + 2, padx=5, pady=5)
        lb2 = Label(show_db_frame, bg='#A8B2C8', font=self.font, text='Add User to Database')
        lb2.grid(column=0, columnspan=4, row=len(txtsample) + 2, sticky='nsew', padx=5, pady=5)
        ent_txt_var = [StringVar(show_db_frame) for _ in range(4)]
        for i in range(4):
            add_ent[i] = Entry(show_db_frame, textvariable=ent_txt_var[i], font=self.font, justify='center')
            add_ent[i].grid(column=i, row=len(txtsample) + 4, sticky='nsew', padx=5, pady=5)
        abutt = Button(show_db_frame, image=self.add_img, bg='#394B59', borderwidth=0, activebackground='#394B59',
                       command=lambda: self.add_user(ent_txt_var))
        abutt.grid(column=4, row=len(txtsample) + 4, padx=5, pady=5)
        self.active_frame = show_db_frame

    def get_db_users(self):
        data = self.pin_decryptor.databasemanager.get_records()
        data = [d for d in data]
        return data

    def add_user(self, user_pack):
        numeric_cond = [0, 2, 3]
        if len(user_pack) == 4:
            condition = True
            for u in range(4):
                if len(user_pack[u].get()) == 0:
                    condition = False
                    break
                elif u in numeric_cond and not user_pack[u].get().isnumeric():
                    condition = False
                    break
            if condition:
                self.pin_decryptor.add_user(user_pack[0].get(), user_pack[1].get(), user_pack[2].get(),
                                            user_pack[3].get())
                self.manage_users_frame()

    def delete_user(self, uid):
        self.pin_decryptor.delete_user(uid)
        self.manage_users_frame()

    def encrypt_cypher_frame(self):
        self.clear_and_reset()
        encrypt_cypher_frame = Frame(self, bg='#394B59')
        encrypt_cypher_frame.grid(column=1, row=0, sticky='nsew')
        for i in range(2):
            encrypt_cypher_frame.columnconfigure(i, weight=1, uniform='1')
        for j in range(7):
            encrypt_cypher_frame.rowconfigure(j, weight=1, uniform='1')
        encrypt_cypher_frame.grid_propagate(False)
        lab1 = Label(encrypt_cypher_frame, bg='#D3D9FB', fg='red', textvariable=self.debug_info, font=self.mid_font)
        lab1.grid(column=0, columnspan=2, row=0, sticky='nsew', padx=5, pady=5)
        lab2 = Label(encrypt_cypher_frame, bg='#D3D9FB', text='Cypher to encrypt:', font=self.mid_font)
        lab2.grid(column=0, row=1, sticky='nsew', padx=5, pady=5)
        cipher_var = StringVar(encrypt_cypher_frame)
        id_var = StringVar(encrypt_cypher_frame)
        pub_var = StringVar(encrypt_cypher_frame)
        range_var = StringVar(encrypt_cypher_frame)
        encrypt_var = StringVar(encrypt_cypher_frame)
        ent_cipher = Entry(encrypt_cypher_frame, bg='#E3E9FF', textvariable=cipher_var, font=self.mid_font,
                           justify='center')
        ent_cipher.grid(column=1, row=1, sticky='nsew', padx=5, pady=5)
        butt1 = Button(encrypt_cypher_frame, bg='#A8B2C8', text='Get user data by Id', font=self.mid_font,
                       command=lambda: self.get_data_by_id(id_var, pub_var, range_var))
        butt1.grid(column=0, row=2, sticky='nsew', padx=5, pady=5)
        ent_id = Entry(encrypt_cypher_frame, bg='#E3E9FF', textvariable=id_var, font=self.mid_font, justify='center')
        ent_id.grid(column=1, row=2, sticky='nsew', padx=5, pady=5)
        lab3 = Label(encrypt_cypher_frame, bg='#D3D9FB', text='Public Key', font=self.mid_font)
        lab3.grid(column=0, row=3, sticky='nsew', padx=5, pady=5)
        lab4 = Label(encrypt_cypher_frame, bg='#D3D9FB', text='Range', font=self.mid_font)
        lab4.grid(column=1, row=3, sticky='nsew', padx=5, pady=5)
        ent_pubkey = Entry(encrypt_cypher_frame, bg='#E3E9FF', textvariable=pub_var, font=self.mid_font, justify='center')
        ent_pubkey.grid(column=0, row=4, sticky='nsew', padx=5, pady=5)
        ent_range = Entry(encrypt_cypher_frame, bg='#E3E9FF', textvariable=range_var, font=self.mid_font, justify='center')
        ent_range.grid(column=1, row=4, sticky='nsew', padx=5, pady=5)
        butt2 = Button(encrypt_cypher_frame, bg='#A8B2C8', text='Generate encrypted cypher', font=self.mid_font,
                       command=lambda: self.encrypt_cypher(pub_var, range_var, cipher_var, encrypt_var))
        butt2.grid(column=0, columnspan=2, row=5, sticky='nsew', padx=5, pady=5)
        lab5 = Label(encrypt_cypher_frame, bg='#D3D9FB', textvariable=encrypt_var, font=self.mid_font)
        lab5.grid(column=0, columnspan=2, row=6, sticky='nsew', padx=5, pady=5)
        self.active_frame = encrypt_cypher_frame

    def get_data_by_id(self, id_var, pub_var, ran_var):
        if len(id_var.get()) > 0:
            values = self.pin_decryptor.databasemanager.get_record(id_var.get())
            if values is not None and len(values) == 2:
                pub_var.set(values[0])
                ran_var.set(values[1])
                self.debug_info.set('')
            else:
                pub_var.set('')
                ran_var.set('')
                self.debug_info.set('Invalid user Id')
        else:
            self.debug_info.set('Empty id value')
            pub_var.set('')
            ran_var.set('')

    def encrypt_cypher(self, pub_var, range_var, cipher_var, encrypt_var):
        val = DecryptorMath.encrypt_cypher(pub_var.get(), range_var.get(), cipher_var.get())
        if type(val) == int:
            encrypt_var.set(val)
        else:
            self.debug_info.set(val)

    def decrypt_cypher_frame(self):
        self.clear_and_reset()
        decrypt_cypher_frame = Frame(self, bg='#394B59')
        decrypt_cypher_frame.grid(column=1, row=0, sticky='nsew')
        for i in range(2):
            decrypt_cypher_frame.columnconfigure(i, weight=1, uniform='1')
        for j in range(7):
            decrypt_cypher_frame.rowconfigure(j, weight=1, uniform='1')
        decrypt_cypher_frame.grid_propagate(False)
        encrypted_cypher_var = StringVar()
        pub_key_var = StringVar()
        range_var = StringVar()
        priv_key_var = StringVar()
        cypher_var = StringVar()
        debug_label = Label(decrypt_cypher_frame, bg='#D3D9FB', fg='red', textvariable=self.debug_info, font=self.mid_font)
        debug_label.grid(column=0, columnspan=2, row=0, sticky='nsew', padx=5, pady=5)
        encrypted_cypher_label = Label(decrypt_cypher_frame, bg='#D3D9FB', text='Encrypted cypher:', font=self.mid_font)
        encrypted_cypher_label.grid(column=0, row=1, sticky='nsew', padx=5, pady=5)
        encrypted_cypher_entry = Entry(decrypt_cypher_frame, bg='#E3E9FF', textvariable=encrypted_cypher_var,
                                       font=self.mid_font, justify='center')
        encrypted_cypher_entry.grid(column=1, row=1, sticky='nsew', padx=5, pady=5)
        get_id_button = Button(decrypt_cypher_frame, bg='#A8B2C8', text='Get your decryption data', font=self.mid_font,
                               command=lambda: self.get_decryption_data(pub_key_var, range_var))
        get_id_button.grid(column=0, columnspan=2, row=2, sticky='nsew', padx=5, pady=5)
        pub_key_label = Label(decrypt_cypher_frame, bg='#D3D9FB', text='Public key:', font=self.mid_font)
        pub_key_label.grid(column=0, row=3, sticky='nsew', padx=5, pady=5)
        pub_key_entry = Entry(decrypt_cypher_frame, bg='#E3E9FF', textvariable=pub_key_var,
                              font=self.mid_font, justify='center')
        pub_key_entry.grid(column=1, row=3, sticky='nsew', padx=5, pady=5)
        range_label = Label(decrypt_cypher_frame, bg='#D3D9FB', text='Range:', font=self.mid_font)
        range_label.grid(column=0, row=4, sticky='nsew', padx=5, pady=5)
        range_entry = Entry(decrypt_cypher_frame, bg='#E3E9FF', textvariable=range_var,
                            font=self.mid_font, justify='center')
        range_entry.grid(column=1, row=4, sticky='nsew', padx=5, pady=5)
        priv_key_label = Label(decrypt_cypher_frame, bg='#D3D9FB', text='Private key:', font=self.mid_font)
        priv_key_label.grid(column=0, row=5, sticky='nsew', padx=5, pady=5)
        priv_key_entry = Entry(decrypt_cypher_frame, bg='#E3E9FF', textvariable=priv_key_var,
                               font=self.mid_font, justify='center')
        priv_key_entry.grid(column=1, row=5, sticky='nsew', padx=5, pady=5)
        decrypt_button = Button(decrypt_cypher_frame, bg='#A8B2C8', text='Decrypt cypher', font=self.mid_font,
                                command=lambda: self.decrypt_cypher(priv_key_var, encrypted_cypher_var, range_var,
                                                                    cypher_var))
        decrypt_button.grid(column=0, row=6, sticky='nsew', padx=5, pady=5)
        cypher_label = Label(decrypt_cypher_frame, bg='#D3D9FB', textvariable=cypher_var, font=self.mid_font)
        cypher_label.grid(column=1, row=6, sticky='nsew', padx=5, pady=5)
        self.active_frame = decrypt_cypher_frame

    def get_decryption_data(self, pub_key, _range):
        values = self.pin_decryptor.get_data()
        if len(values) == 2:
            pub_key.set(values[0])
            _range.set(values[1])

    def decrypt_cypher(self, priv_key, encrypted_cypher, _range, cypher):
        val = encrypted_cypher.get()
        priv = priv_key.get()
        _range = _range.get()
        cypher.set(DecryptorMath.decrypt_cipher(val, _range, priv))

    def show_help_frame(self):
        self.clear_and_reset()
        frame1 = Frame(self, bg='#394B59')
        frame1.grid(row=0, column=1, sticky='nsew')
        frame1.rowconfigure(0, weight=1, uniform='1')
        frame1.rowconfigure(1, weight=9, uniform='1')
        frame1.columnconfigure(0, weight=1, uniform='1')
        frame1.grid_propagate(False)
        self.configure_top_frame(frame1)
        self.configure_help_frame(frame1)
        self.active_frame = frame1

    def configure_top_frame(self, parent):
        top_frame = Frame(parent, bg='#394B59')
        top_frame.grid(row=0, column=0, sticky='nsew')
        top_frame.grid_propagate(False)
        top_frame.rowconfigure(0, weight=1, uniform='1')
        top_frame.columnconfigure(0, weight=1, uniform='1')
        top_frame.columnconfigure(1, weight=5, uniform='1')
        top_frame.columnconfigure(2, weight=1, uniform='1')
        top_title = StringVar()
        self.set_title(top_title)
        lab = Label(top_frame, bg='#E3E9FF', textvariable=top_title, font=self.font)
        lab.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        button1 = Button(top_frame, bg='#394B59', image=self.prev_img, borderwidth=0, activebackground='#394B59',
                         command = lambda: self.update_help_mode(top_title, '-'))
        button1.grid(row=0, column=0, sticky='nsew')
        button2 = Button(top_frame, bg='#394B59', image=self.next_img, borderwidth=0, activebackground='#394B59',
                         command = lambda: self.update_help_mode(top_title, '+'))
        button2.grid(row=0, column=2, sticky='nsew')

    def configure_help_frame(self, parent):
        help_size = int(1366 / self.winfo_screenwidth() * 19)
        fon = font.Font(family='courier', size=help_size, weight='bold')
        help_frame = Frame(parent, bg='#394B59')
        help_frame.grid(row=1, column=0, sticky='nsew')
        help_frame.grid_propagate(False)
        help_frame.columnconfigure(0, weight=1, uniform='1')
        help_frame.columnconfigure(1, weight=1, uniform='1')
        help_frame.rowconfigure(0, weight=1, uniform='1')
        self.help_text.set(self.get_help_text())
        lab = Label(help_frame, bg='#E3E9FF', textvariable=self.help_text, font=fon, justify='left')
        lab.grid(row=0, column=0, columnspan=2, sticky='nsew', padx=5, pady=5)

    def update_help_mode(self, top_title, sign=''):
        if sign == '+' and self.help_mode < 5:
            self.help_mode += 1
            self.set_title(top_title)
        elif sign == '-' and self.help_mode > 1:
            self.help_mode -= 1
            self.set_title(top_title)
        self.help_text.set(self.get_help_text())

    def set_title(self, title):
        match self.help_mode:
            case 1:
                title.set('Program description')
            case 2:
                title.set('Creating your Id data')
            case 3:
                title.set('Managing Users')
            case 4:
                title.set('Cypher encryption')
            case 5:
                title.set('Cypher decryption')

    def get_help_text(self):
        match self.help_mode:
            case 1:
                return '''- Numeric decryptor is a program, which allow you to
  encryption and decryption numeric cyphers
- Encryption is based on an asynchronic cryptograpy algorithm RSA
- The program has the following functionalities (Top-left part):
    ~ Creating ID
    ~ Users management
    ~ Encryption and decryption cyphers
    ~ Help panel
- On the bottom-left part you can see your Id data,
  which are necessary to decryption numeric messages
  sent to you by other users'''
            case 2:
                return '''- Create your Id is an option needed to create your public data
- This is necessary step if you want to decrypt messages
- On the top of this panel is a debug info
- Debug info will notify you if you type incorrect data
- The maximum range is 99999 because of computational restrictions
- Choose the minimum range you want to handle and press generate Id
- Program will create your data randomly
- Some of data (public key and range) will be saved in file
- Send this data to your friends to allow them
  to encrypt numeric cyphers to you
- Private key is and essential element of your data
  and it will be used for cyphers decryption
- It need to be secured (It is recommended to keep it offline)
'''
            case 3:
                return '''- On the manage users tab you can adding and removing users
- It allow to save a public data of your friends in database
- You 'll use it to encrypt cyphers to them in the future
- To add an user, you need to fill an entry places on the bottom
- Public key and range are generated by your friend
- Remember, that range is and upper limit of cypher to encrypt
- Nick is an alias of your friend
- Id is used for ordering friends in database (ascending order)
- It is recommended to use small numbers for important users
- Fill all entrance fields and press the add button
- If all data are correct, new user will be added to database
- You can also delete user by pressing remove button next to him'''
            case 4:
                return '''- Encrypt cypher option show as a panel
  in which you can to encrypt numeric cyphers to your friends
- Type numeric value next to 'cypher to encrypt' label
- In next step you need to fill pubic key and range of your friend
- You can get this data by Id if you saved your friend in database
- Remember that your cypher needs to be smaller than range value
- Otherwise this cypher cannot be decoded by your friend
- On the end generate encrypted cypher and send it to your friend'''
            case 5:
                return '''- Decrypt cypher panel allow you to decode cyphers you received
- Paste it next to encrypted cypher label
- In the next step fill all of your data
- The public data are visible in left bottom part
- You can get this data also by button
- After filling all fields you can decrypt transferred data'''

