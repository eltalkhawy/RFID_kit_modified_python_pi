code_Row = "030c1020c0"
my_hex = code_Row.decode('hex')

for bit in range(0, len(code_Row)):	
    print''.join(hex(ord(n)) for n in (0x80 & (my_hex << bit)))
