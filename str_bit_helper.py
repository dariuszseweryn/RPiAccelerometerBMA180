def bits2str(data):
    return ''.join(chr(int(''.join(x),2)) for x in zip(*[iter(data)]*8))

def str2bits(string):
    return bin(reduce(lambda x, y : (x<<8)+y, (ord(c) for c in string), 1))[3:]

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
