def strToBinStr(str):
    '''Return string as a binary string'''
    hexString = str.encode('utf_8','ignore').hex()
    
    return ''.join(['{:08b}'.format(int(hexString[x*2:(x+1)*2],16)) for x in range(0,round(len(hexString)/2))])

def strToBinArr(str):
    '''Return string as a binary array'''
    hexString = str.encode('utf_8','ignore').hex()

    return ['{:08b}'.format(int(hexString[x*2:(x+1)*2],16)) for x in range(0,round(len(hexString)/2))]

def binArrToStr(bin):
    '''Return binary array as a string'''
    return b''.join([int(x,2).to_bytes(1, byteorder='big') for x in bin]).decode()

def binStrToStr(bin):
    '''Return binary string as a string'''
    bytes = [bin[x*8:(x+1)*8] for x in range (0, round ((len(bin) / 8)))]

    return b''.join([int(x,2).to_bytes(1, byteorder='big') for x in bytes]).decode()