def tally_token_transfer(log_emission):
    # Dictionary to hold the tally
    tally = {}
    for log in log_emission:
        if log['topics'][0]!='0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef':
            continue
            
        # Extracting the relevant data
        token_address = log['address']
        from_address = '0x' + log['topics'][1][-40:]
        to_address = '0x' + log['topics'][2][-40:]
        amount = int(log['data'], 16)

        # Adjusting for the sender
        if from_address not in tally:
            tally[from_address] = {}
        if token_address not in tally[from_address]:
            tally[from_address][token_address] = 0
        tally[from_address][token_address] -= amount

        # Adjusting for the receiver
        if to_address not in tally:
            tally[to_address] = {}
        if token_address not in tally[to_address]:
            tally[to_address][token_address] = 0
        tally[to_address][token_address] += amount

    return tally

def decode_univ2_info(raw_value):
    raw_value=raw_value[2:]
    print(raw_value)
    _reserve0_hex = raw_value[:64]
    _reserve0 = hex(int(_reserve0_hex,16))

    # Parsing _reserve1
    _reserve1_hex = raw_value[64:128]
    _reserve1 = hex(int(_reserve1_hex,16))

    return _reserve0,_reserve1