import time
import sys
from interface_spi import InterfaceSPI
from accelerometer import Accelerometer
from str_bit_helper import *

interface = None
acc = None

def configure():
    global interface, acc
    interface = InterfaceSPI(InterfaceSPI.CE_1, InterfaceSPI.SPEED_16_0MHZ)
    acc = Accelerometer(interface)
    acc.add_callback(acc_value_callback)
    print('Main program configuration finished')

def acc_value_callback(x,y,z):
    print('x= %s\ty= %s\tz= %s' % (
            float_to_string(to_angle(x),6),
            float_to_string(to_angle(y),6),
            float_to_string(to_angle(z),6)
            )
          )
    
def run():
    while(True):
        try:    
            time.sleep(1)
        except KeyboardInterrupt:
            manual_mode()

def manual_mode():
    acc.set_notify(False)
    print('\n>>> Switched to manual mode <<<')
    should_exit = False
    while(not should_exit):
        variable = raw_input('what to send? (\'help\' for help): ')
        if (variable == 'help'):
            print('(r/w, address, data)\n' +
                  '\'r\' - read, \'w\' - write\n' +
                  'address - a byte (bin or hex) of address to r/w\n' +
                  'data - (optional) a byte (bin or hex) to write\n' +
                  'type \'exit\' to finish program')
        elif(variable == 'exit'):
            sys.exit(0)
        elif(len(variable) > 0):
            parts = variable.split(' ')
            r_w = parts.pop(0)
            if (r_w != 'r' and r_w != 'w'):
                break
            else:
                read_write = (r_w == 'r')
                
            address = parse_int_string_to_bin_string(parts.pop(0))

            data = ('00111111' if read_write else parse_int_string_to_bin_string(parts.pop(0)))

            if (len(address) != 8 or len(data) != 8):
                print('Illegal data to %s address:%s data:%s' % (
                    'read from' if read_write else 'write to',
                    address,
                    data
                    )
                      )
                break

            print(int(round(time.time() * 1000000)))
            returned_data = interface.send(read_write, bits2str(address), bits2str(data))
            print(int(round(time.time() * 1000000)))

            if(read_write):
                print(str2bits(returned_data))
        else:
            should_exit = True
    print('\n>>>  Switched back to loop  <<<')
    acc.set_notify(True) 

def main(arguments):
    configure()
    run()

if __name__ == "__main__":
    main(sys.argv)
        
