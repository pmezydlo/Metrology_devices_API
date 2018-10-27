#! /usr/bin/env python3
# -*- coding: utf-8 -*-

'''

'''

__author__ = "Patryk Mezydlo"
__copyright__ = "Copyright 2018, Metrology Device API"
__credits__ = ["Patryk Mezydlo"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Patryk Mezydlo"
__email__ = "mezydlo.p@gmail.com"
__status__ = "Development"

import time
from common_const import *

def delay(dev, args):
    time.sleep(int(args))
    return 'ok'

def screen(dev, args):
    dev.write(':DISP:DATA?')
    bmp_data = dev.read_raw()[2+9:]

    with open(FILES_PATH()+args, "wb") as f:
        f.write(bmp_data)
    return 'Saved'

entry_array = {'delay':delay,
               'screen':screen}

