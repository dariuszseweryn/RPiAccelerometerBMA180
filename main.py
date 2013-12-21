from __future__ import division

import time
import sys, os
from interface_spi import InterfaceSPI
from accelerometer import Accelerometer
from str_bit_helper import *

class MainProgram():

    def __init__(self):
        self.console_logger = ConsoleLogger()
        self.file_logger = FileLogger('acc_output.txt')
        self.interface = InterfaceSPI(InterfaceSPI.CE_1, InterfaceSPI.SPEED_16_0MHZ)
        self.acc = Accelerometer(self.interface)
        self.acc.add_callback(self.console_logger.log)
        self.acc.add_callback(self.file_logger.log)
        print('Main program configuration finished')
        
    def run(self):
        while(True):
            try:    
                time.sleep(1)
            except KeyboardInterrupt:
                self.manual_mode()

    def manual_mode(self):
        print('\n>>> Switched to manual mode <<<')
        self.console_logger.set_on(False)
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

                returned_data = self.interface.send(read_write, bits2str(address), bits2str(data))

                if(read_write):
                    print(str2bits(returned_data))
            else:
                should_exit = True
        print('\n>>>  Switched back to loop  <<<')
        self.console_logger.set_on(True)

class ConsoleLogger():
    count_threshold = 30

    def __init__(self):
        self.on = True
        self.values = [0,0,0]
        self.count = 0
        
    def log(self,x,y,z):
        new_values = (x,y,z)
        self.values = [a + b for a, b in zip(self.values, new_values)]
        self.count += 1
        if (self.count >= ConsoleLogger.count_threshold and self.on):
            print(
                'x= %s\ty= %s\tz= %s' %
                tuple([float_to_string(to_angle(a/self.count), 6) for a in self.values])
            )
            self.values = [0,0,0]
            self.count = 0

    def set_on(self,on):
        self.on = on

class FileLogger():
    file_name = 'acc_results.txt'
    
    def __init__(self, file_name):
        try:
            self.start_time = time.time() * 1000
            os.system('touch %s' % file_name)
            os.system('chmod 644 %s' % file_name)
            self.file = open(file_name, 'w')
        except IOError:
            print('Could not open file: %s' % file_name)
            sys.exit(1)

    def log(self,x,y,z):
        if not self.file.closed:
            self.file.write('%d\t%d\t%d\t%d\n' % (time.time() * 1000 - self.start_time,x,y,z))
            

def main(arguments):
    MainProgram().run()

if __name__ == "__main__":
    main(sys.argv)
        
