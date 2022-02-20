from tkinter import Tk, Frame, Button, ttk


class appwindow(Tk):

    def __init__(self):
        super().__init__()
        self.geometry('1920x1080')
        self.title('Numeric Decryptor')

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)

        self.menu_frame()

    def clear_elements(self, frame):
        list = frame.grid_slaves()
        for l in list:
            l.destroy()


    def menu_frame(self):
        f1 = Frame(self)
        f1.grid(row = 0, column = 0)
        b1 = Button(f1, text = 'abc', command = lambda: self.add_user_frame())
        b1.grid(row = 0)

    def add_user_frame(self):
        f2 = Frame(self)
        f2.grid(row = 0, column = 1)
        b2 = Button(f2, text = 'cfg', command = lambda: self.delete_user_frame(f2))
        b2.grid(row = 0)

    def delete_user_frame(self, lastframe):
        self.clear_elements(lastframe)
        f3 = Frame(self)
        f3.grid(row = 0, column = 1)
        b3 = Button(f3, text = 'qwe', command = lambda: self.add_user_frame(f3))
        b3.grid(row = 0)


