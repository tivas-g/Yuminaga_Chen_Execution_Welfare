def decode4makeraddress(call_data):
    # Ethereum data fields are 64 characters long
    field_length = 64

    start_pos = field_length * 12 + 10

    # Extract the 12th field
    field_raw = call_data[start_pos:start_pos + field_length]

    # The actual address is the last 40 characters, remove leading zeros
    address = '0x' + field_raw[-40:]

    return address

def decode4receipientaddress(call_data):
    # Ethereum data fields are 64 characters long
    field_length = 64

    start_pos = field_length * 13 + 10

    # Extract the 12th field
    field_raw = call_data[start_pos:start_pos + field_length]

    # The actual address is the last 40 characters, remove leading zeros
    address = '0x' + field_raw[-40:]

    return address

def decode4inputassetaddress(call_data):
    # Ethereum data fields are 64 characters long
    field_length = 64

    start_pos = field_length * 10 + 10

    # Extract the 12th field
    field_raw = call_data[start_pos:start_pos + field_length]

    # The actual address is the last 40 characters, remove leading zeros
    address = '0x' + field_raw[-40:]

    return address

def decode4outputassetaddress(call_data):
    # Ethereum data fields are 64 characters long
    field_length = 64

    start_pos = field_length * 11 + 10

    # Extract the 12th field
    field_raw = call_data[start_pos:start_pos + field_length]

    # The actual address is the last 40 characters, remove leading zeros
    address = '0x' + field_raw[-40:]

    return address

def decode4takeraddress(call_data):
    # Ethereum data fields are 64 characters long
    field_length = 64

    start_pos = field_length * 8 + 10

    # Extract the 12th field
    field_raw = call_data[start_pos:start_pos + field_length]

    # The actual address is the last 40 characters, remove leading zeros
    address = '0x' + field_raw[-40:]

    return address

def decode4inputamount(call_data):
    # Ethereum data fields are 64 characters long
    field_length = 64

    start_pos = field_length * 5 + 10

    # Extract the 12th field
    field_raw = call_data[start_pos:start_pos + field_length]
    field_raw = hex(int(field_raw,16))
    return field_raw