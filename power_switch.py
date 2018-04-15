import Adafruit_BBIO.GPIO as GPIO

class power_switch(object):
    pins = {
        1 : {'phy_name' : 'P8_10'},
        2 : {'phy_name' : 'P8_11'},
        3 : {'phy_name' : 'P9_12'},
        4 : {'phy_name' : 'P9_13'},
        5 : {'phy_name' : 'P9_14'},
        6 : {'phy_name' : 'P9_15'}, 
        7 : {'phy_name' : 'P9_16'},
        8 : {'phy_name' : 'P9_17'}}

    def __init__ (self):
        for pin in pins:
            GPIO.setup(pin['phy_name'], GPIO.OUT)
            
    def channel_on (self, channel_num):
        GPIO.output(pins[channel_num]['phy_name'], GPIO.HIGH)

    def channel_off (self, channel_num):
        GPIO.output(pins[channel_num]['phy_name'], GPIO.LOW)

    def get_channel_state (self, channel_num):
        if GPIO.input(pins[channel_num]['phy_name']) == GPIO.LOW:
            return 0
        else
            return 1
