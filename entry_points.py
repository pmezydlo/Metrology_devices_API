import time

def delay(dev, args):
    time.sleep(int(args))
    return 'ok'

def screen(dev, args):
    dev.write(":DISP:DATA?")
    bmp_data = dev.read_raw()[2+9:]

    with open("files/"+args, "wb") as f:
        f.write(bmp_data)
    return 'Saved'

entry_array = {'delay':delay,
               'screen':screen}

