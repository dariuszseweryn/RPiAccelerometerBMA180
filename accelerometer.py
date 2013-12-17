# -*- coding: utf-8 -*-

from __future__ import division
import sys, os, math
import RPi.GPIO as GPIO
from str_bit_helper import *

GP_DATA_READY_INT_PIN = 22

# using Bosch's BMA180 - 3-axial MEMS accelerometer
class Accelerometer():
    ACCUMULATOR_COUNT = 30

    # technically almost ready to use I2C if provided
    def __init__(self, interface):
        self.read_acc_values_address = bits2str(fill_bits_to_byte(bin(0x02)[2:]))
        self.interface = interface
        self.callbacks = set()
        self.acc_x = 0
        self.acc_y = 0
        self.acc_z = 0
        self.acc_count = 0
        self.notify = True
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(GP_DATA_READY_INT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(
            GP_DATA_READY_INT_PIN,
            GPIO.RISING,
            callback=self.accelerometer_int
            )
        # allow changing configuration (originally 0x00)
        interface.send(False, int2char(0x0D), int2char(0x10))
        # cutting bandwidth <10Hz to get better SNR (0x48)
        interface.send(False, int2char(0x20), int2char(0x08))
        # disable i2c (0x64)
        # interface.send(False, int2char(0x27), int2char(0x65))
        # set range to +/- 1G (0x54) 
        interface.send(False, int2char(0x35), int2char(0x51))
        # set interrupts on new data available (0x04)
        interface.send(False, int2char(0x21), int2char(0x02))
        # all changes are temporary (till power off), no saving added
        self.__read_acc()
        print('Accelerometer initialized with interface ' + str(interface))
        
    def __read_acc(self):
        return self.interface.send(True, self.read_acc_values_address, '??????')

    def accelerometer_int(self, channel):
        x,y,z = self.read_accelerometer_values()
        self.acc_x += x
        self.acc_y += y
        self.acc_z += z
        self.acc_count += 1
        if self.acc_count > Accelerometer.ACCUMULATOR_COUNT:
            x = self.acc_x / self.acc_count
            y = self.acc_y / self.acc_count
            z = self.acc_z / self.acc_count
            self.acc_x = 0
            self.acc_y = 0
            self.acc_z = 0
            self.acc_count = 0
            if self.notify:
                for callback in self.callbacks:
                    callback(x,y,z)
        
    def read_accelerometer_values(self):
        read_data = self.__read_acc()
        x_value = self.__get_value(read_data[1:2], read_data[0:1])
        y_value = self.__get_value(read_data[3:4], read_data[2:3])
        z_value = self.__get_value(read_data[5:6], read_data[4:5])
        return (x_value, y_value, z_value)

    def add_callback(self, callback):
        self.callbacks.add(callback)

    def remove_callback(self, callback):
        self.callbacks.remove(callback)

    def set_notify(self, notify):
        self.notify = notify
        
    def __get_value(self, high_byte_char, low_byte_char):
        value = str2bits(high_byte_char) + str2bits(low_byte_char)[:-2]
        int_value = int(value, 2)
        if (int_value >= (1 << 13)):
            int_value -= (1 << 14)
        return int_value
