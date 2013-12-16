# -*- coding: utf-8 -*-

from __future__ import division
import sys, os, math
import RPi.GPIO as GPIO
from bitstring import Bits
from ctypes import *
wiringpi_path = os.path.abspath('WiringPi-Python')
print(wiringpi_path)
sys.path.append( wiringpi_path )
import wiringpi2 as wiringpi

GP_DATA_READY_INT_PIN = 22

print_result = True
acc_x = 0
acc_y = 0
acc_z = 0
acc_count = 0

#class Accelerometer():
#
#    def __init__(self, spi_interface, ce_pin, int_pin=None):
        

def configure():
    os.system('gpio load spi')
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(GP_DATA_READY_INT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(GP_DATA_READY_INT_PIN, GPIO.RISING, callback=accelerometer_int)
    wiringpi.wiringPiSetup()
    error = wiringpi.wiringPiSPISetup(1,1500000)
    if (error == -1):
        print('Error while SPI Setup')
        return

    spi_send(read_acc_str())    
    print('SPI configured')

def read_acc_str():
    return bits2str(bin(0x82 << 6*8)[2:])

def accelerometer_int(channel):
    global acc_x, acc_y, acc_z, acc_count
    x,y,z = read_accelerometer_values()
    acc_x += x
    acc_y += y
    acc_z += z
    acc_count += 1
    #print(print_result)
    if(print_result == True and acc_count >= 30):
        print('x= %s\ty= %s\tz= %s' % (
                float_to_string(to_angle(float(acc_x/acc_count)),5),
                float_to_string(to_angle(float(acc_y/acc_count)),5),
                float_to_string(to_angle(float(acc_z/acc_count)),5))
            )
        acc_x = 0
        acc_y = 0
        acc_z = 0
        acc_count = 0

def read_accelerometer_values():
    data = spi_send(read_acc_str())
    read_data = data[1:]
    x_value = get_value(read_data[1:2], read_data[0:1])
    y_value = get_value(read_data[3:4], read_data[2:3])
    z_value = get_value(read_data[5:6], read_data[4:5])
    return (x_value, y_value, z_value)

def set_print_result(boolean):
    global print_result
    print_result = boolean
    spi_send(bits2str(bin(0x82 << 6*8)[2:]))

def spi_send(data):
    data_cpy = data[:]
    error = wiringpi.wiringPiSPIDataRW(1, data_cpy)
    if (error == -1):
        print('send SPI error')
        return None
    return data_cpy

def bits2str(data):
    return ''.join(chr(int(''.join(x),2)) for x in zip(*[iter(data)]*8))

def str2bits(string):
    return bin(reduce(lambda x, y : (x<<8)+y, (ord(c) for c in string), 1))[3:]

def get_byte(byte_index, long_bit_string):
    start = byte_index * 8
    byte_string = long_bit_string[start:start + 8]
    return int(byte_string,2)

def get_value(high_byte_char, low_byte_char):
    value = str2bits(high_byte_char) + str2bits(low_byte_char)[:-2]
    #print(value)
    #return Bits(bin=value).int
    int_value = int(value, 2)
    if (int_value >= (1 << 13)):
        int_value -= (1 << 14)
    return int_value

def to_angle(x):
    return math.degrees(math.asin(float(x/8192)))

def float_to_string(float_value, string_length):
    string_value = ('%.2f' % float_value)
    characters_to_add = string_length - len(string_value)
    return_string = ''
    if (characters_to_add > 0):
        for i in range(0,characters_to_add):
            return_string += ' '
    return_string += string_value
    return return_string
