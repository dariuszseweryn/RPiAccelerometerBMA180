import os
wiringpi_path = os.path.abspath('WiringPi-Python')
print(wiringpi_path)
sys.path.append( wiringpi_path )
import wiringpi2 as wiringpi
from str_bit_helper import *

class SpiInterface():

    def __main__(self):
        os.system('gpio load spi')
        wiringpi.wiringPiSetup()
        error = wiringpi.wiringPiSPISetup(1,1500000)
        if (error == -1):
            raise SetupException('Error while SPI setup')

    def send(self, read_write, address_char, string_data, channel):
        if (read_write):
            address_bin = fill_bits_to_byte(str2bits(address_char))[
            address_char = bits2str('1' + address_bin)
        string_data_cpy = address_char + string_data[:]
        error = wiringpi.wiringPiSPIDataRw()
        if (error == -1):
            error_msg = (
                'Error while SPI %s address:%s data:%s' % (
                    'read' if read_write else 'write',
                    str2bits(address_char),
                    '(not important)' if read_write else str2bits(string_data)
                    )
                )
            raise SendingException(error_msg)
        return string_data_cpy[1:] if read_write else None
