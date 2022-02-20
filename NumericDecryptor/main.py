from pinDecryptor import PinDecryptor
from appwindow import appwindow


if __name__ == '__main__':
    pd = PinDecryptor()
    root = appwindow()
    root.mainloop()
    condition = -1
    while condition != 0:
        condition = pd.switch_loop()
