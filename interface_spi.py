import os, sys
from my_exceptions import SetupException, SendingException
from str_bit_helper import *
wiringpi_path = os.path.abspath('WiringPi-Python')
sys.path.append( wiringpi_path )
import wiringpi2 as wiringpi

class InterfaceSPI():
    CE_0 = 0
    CE_1 = 1
    SPEED_0_5MHZ = 500000
    SPEED_1_0MHZ = 2 * SPEED_0_5MHZ
    SPEED_2_0MHZ = 2 * SPEED_1_0MHZ
    SPEED_4_0MHZ = 2 * SPEED_2_0MHZ
    SPEED_8_0MHZ = 2 * SPEED_4_0MHZ
    SPEED_16_0MHZ = 2 * SPEED_8_0MHZ
    SPEED_32_0MHZ = 2 * SPEED_16_0MHZ

    def __init__(self, ce_channel, speed):
        self.ce_channel = ce_channel
        os.system('gpio load spi')
        wiringpi.wiringPiSetup()
        error = wiringpi.wiringPiSPISetup(ce_channel,speed)
        if (error == -1):
            raise SetupException('Error while SPI setup')
        print('InterfaceSPI initalized (CE_%d, speed:%.1fMHz)' % (ce_channel, speed * 0.000001))

    def send(self, read_write, address_char, string_data):
        if (read_write):
            address_bin = fill_bits_to_byte(str2bits(address_char))
            address_char = bits2str('1' + address_bin[1:])
        string_data_cpy = address_char + string_data[:]
        error = wiringpi.wiringPiSPIDataRW(self.ce_channel, string_data_cpy)
        if (error == -1):
            #error_msg = SendingException.get_msg(read_write, address_char, string_data)
            error_msg = (
                'Error while SPI %s address:%s data:%s' % (
                    'read' if read_write else 'write',
                    str2bits(address_char),
                    '(not important)' if read_write else str2bits(string_data)
                )
            )
            raise SendingException(error_msg)
        return string_data_cpy[1:] if read_write else None

    def __unicode__(self):
        return self.__str__()
    def __repr__(self):
        return self.__str__()
    def __str__(self):
        return 'InterfaceSPI'
