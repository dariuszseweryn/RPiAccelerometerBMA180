import time
import sys
import accelerometer
from accelerometer import bits2str, str2bits, spi_send


def configure():
    print('configure')
    accelerometer.configure()

def run():
    print('run')
    while(True):
        try:    
            #accelerometer.accelerometer_int(1)
            time.sleep(1)
        except KeyboardInterrupt:
            manual_mode()

def manual_mode():
    accelerometer.set_print_result(False)
    print('\n>>> Switched to manual mode <<<')
    should_exit = False
    while(not should_exit):
        variable = raw_input('address send: ')
        if(len(variable) > 0):
            parts = variable.split(' ')
            bits_string = ''
            for part in parts:
                bits_string += parse_string(part)
            if(len(bits_string) == 8):
                bits_string += '00111111'
            data = spi_send(bits2str(bits_string))
            print(str2bits(data[1:]))
        else:
            should_exit = True
    print('\n>>>  Switched back to loop  <<<')
    accelerometer.set_print_result(True)

def parse_string(string):
    string_length = len(string)
    if(string_length == 0):
        bits = ''
    if(string_length == 4):
        bits = bin(int(string, 16))[2:]
        bits = fill_bits_to_byte(bits)
    if(string_length == 8):
        bits = string
    return bits

def fill_bits_to_byte(bits):
    length = len(bits)
    byte_bits = ''
    for i in range(0,8-length):
        byte_bits += '0'
    return byte_bits + bits   

def main(arguments):
    configure()
    run()

if __name__ == "__main__":
    main(sys.argv)
        
