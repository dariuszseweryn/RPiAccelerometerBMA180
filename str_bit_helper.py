from my_exceptions import ConvertionException
import math

def bits2str(data):
    if (len(data) % 8 != 0):
        raise ConvertionException('bits2str() data (%s) is not consisting of full bytes' % data)
    return ''.join(chr(int(''.join(x),2)) for x in zip(*[iter(data)]*8))

def str2bits(string):
    return bin(reduce(lambda x, y : (x<<8)+y, (ord(c) for c in string), 1))[3:]

def int2char(int_value):
    return bits2str(fill_bits_to_byte(bin(int_value)[2:]))

def parse_int_string_to_bin_string(string):
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

def to_angle(x):
    return math.degrees(math.asin(float(x/8192)))

def float_to_string(float_value, min_string_length):
    string_value = ('%.2f' % float_value)
    characters_to_add = min_string_length - len(string_value)
    return_string = ''
    if (characters_to_add > 0):
        for i in range(0,characters_to_add):
            return_string += ' '
    return_string += string_value
    return return_string
