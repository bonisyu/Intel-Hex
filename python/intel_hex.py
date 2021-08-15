import sys

# Create a memory map, initial value: 0xFF
map = [0xFF] * (96 * 16)

# Intel-HEX Format
intelHexData = {
    'LENGTH'  : None,
    'ADDR'    : None,
    'RECODE'  : None,
    'DATA'    : [],
    'CHECKSUM': None
}

# Get HEX file, return lines
def f_getIntexHexFile(fileName):
    try:
        with open(fileName):
            print('[SYS] Open File Success.')

    except IOError:
        print('[ERR] Open File Error.')

    fp = open(fileName, 'r')
    ret_lines = fp.readlines()
    fp.close()

    return ret_lines

# Decode Intel-HEX for single line
def f_decodeIntexHexLine(lineData):
    data = []
    r = range(1, len(lineData)-1, 2)
    
    for index in r:
        byte = int(lineData[index:index+2], 16)
        data.append(byte)

    return data

# Print memory map
def f_showMemoryMap(map):
    print('\nMemory Map: ')

    for i in range(0, len(map)):
        if(i % 16 == 0 and i != 0):
            print('')

        if(i % 16 == 0):
            print("{:08X}".format(i), ': ', end = '\t')
            
        print("{:02X}".format(map[i]), end = ' ')


if __name__ == '__main__':
    lines = f_getIntexHexFile('../test_file/test.hex')

    for j in range(len(lines)):
        arr = f_decodeIntexHexLine(lines[j])

        intelHexData['LENGTH']   = arr[0]
        intelHexData['ADDR']     = (arr[1] << 8) | arr[2]
        intelHexData['RECODE']   = arr[3]
        intelHexData['CHECKSUM'] = arr[-1]

        if(intelHexData['CHECKSUM'] == 0x100 - (sum(arr[0:-1]) & 0xFF)):
            print("\r", end="")
            print("[SYS] Progress: {}/{}".format(j+1, len(lines)),end="")
            sys.stdout.flush()

        else:
            print("[ERR] ", 'INTEL HEX ERR (Checksum)')
            break
        
        for index in range(4, intelHexData['LENGTH'] + 4):
            intelHexData['DATA'].append(arr[index])

        for index in range(0, intelHexData['LENGTH']):
            map[ intelHexData['ADDR']+index ] = arr[index+4]

        intelHexData['LENGTH']   = None
        intelHexData['ADDR']     = None
        intelHexData['RECODE']   = None
        intelHexData['CHECKSUM'] = None
        intelHexData['DATA'].clear()
        arr.clear()

    f_showMemoryMap(map)