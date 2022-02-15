from pinDecryptor import PinDecryptor


if __name__ == '__main__':
    pd = PinDecryptor()
    condition = -1
    while condition != 0:
        condition = pd.switch_loop()
