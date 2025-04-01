from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import json
import parseUnixCalldata as parseCalldata
import calcExecution
import numpy as np
import sqlite3
import random


with open('.credentials', 'r') as file:
    credentials = json.load(file)

mongodb_password = credentials.get('MONGODB_PASSWORD')
uri = f""
# Create a new MongoDB client and connect to the server
# client = MongoClient(uri, server_api=ServerApi('1'))

# # Choose a database and a collection in MongoDB
# db = client['rfq-prod']
# collection = db['PEPE']

alchemy_api = credentials.get('ALCHEMY_APIKEY')
infura_api =  credentials.get('INFURA_APIKEY')

import requests
import time

PEPE = '0x6982508145454ce325ddbe47a25d4ec3d2311933'
WETH = '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2'

def fetch_univ2_status(block_no):
    infura_url = f"https://mainnet.infura.io/v3/{infura_api}"

    contract_address = '0xA43fe16908251ee70EF74718545e4FE6C5cCEc9f'

    data_field = '0x0902f1ac' #func selector for getreserve view function
    # Construct the JSON payload
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_call",
        "params": [{
            "to": contract_address,
            "data": data_field
        }, hex(int(block_no)-1)],  # fetch blockno -1
        "id": 1
    }

    # Send POST request to Infura
    response = requests.post(infura_url, json=payload)

    # Check for a valid response
    if response.status_code == 200:
        # Decode the response
        response = response.json()
        return response['result']
    else:
        print("Failed to fetch data. Status code:", response.status_code)


dex_router_list = (
"0xe592427a0aece92de3edee1f18e0157c05861564", #uniswap v3 router01
"0x68b3465833fb72a70ecdf485e0e4c7bd8665fc45", #uniswap v3 router02
"0x1f98415757620b543a52e61c46b32eb19261f984", #uniswap v3 multi call
"0x5ba1e12693dc8f9c48aad8770482f4739beed696", #uniswap v3 multi call2
"0x3fc91a3afd70395cd496c647d5a6cc9d4b2b7fad", #universal router
"0x7a250d5630b4cf539739df2c5dacb4c659f2488d", #uniswap v2 router02
"0xf164fc0ec4e93095b804a4795bbe1e041497b92a", #uniswap v2 router01
"0xd9e1ce17f2641f24ae83637ab66a2cca9c378b9f", #sushiswap v2 router02
"0x111111125421ca6dc452d289314280a0f8842a65", #1inch routerv6
"0x1111111254fb6c44bac0bed2854e76f90643097d", #1inch routerv4
"0x111111125434b319222cdbf8c261674adb56f3ae", #1inch routerv2
"0x1111111254eeb25477b68fb85ed929f73a960582", #1inch routerv5
"0x11111112542d85b3ef69ae05771c2dccff4faa26" #1inch routerv3
)

def fetch_block_gas_info(block_no):
    url = f"https://eth-mainnet.g.alchemy.com/v2/{alchemy_api}"
    payload = {
        "id": 1,
        "jsonrpc": "2.0",
        "method": "eth_getBlockByNumber",
        "params": [hex(int(block_no)),True]
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }

    response = json.loads(requests.post(url, json=payload, headers=headers).content)
    amm_gas = 0
    gas_price_array=[]
    for tx in response['result']['transactions']:
        if tx['to'] in dex_router_list:
            amm_gas=int(tx['gasPrice'],16)
        gas_price_array.append(int(tx['gasPrice'],16))
    
    return gas_price_array,amm_gas

def fetch_tx(tx_hash):
    url = f"https://eth-mainnet.g.alchemy.com/v2/{alchemy_api}"
    payload = {
        "id": 1,
        "jsonrpc": "2.0",
        "method": "eth_getTransactionByHash",
        "params": [tx_hash,]
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }

    response = json.loads(requests.post(url, json=payload, headers=headers).content)
    # print(response)
    return (response['result'])

def fetch_tx_receipt(tx_hash):
    url = f"https://eth-mainnet.g.alchemy.com/v2/{alchemy_api}"
    payload = {
        "id": 1,
        "jsonrpc": "2.0",
        "method": "eth_getTransactionReceipt",
        "params": [tx_hash]
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }

    response = json.loads(requests.post(url, json=payload, headers=headers).content)
    return response['result']['logs']


def upsert_record(db_path, tx_hash, record2write):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Prepare the columns and values for the query
    columns = ', '.join(record2write.keys())
    placeholders = ', '.join(['?'] * len(record2write))
    update_placeholders = ', '.join([f"{key} = ?" for key in record2write.keys()])

    # Construct the SQL query
    query = f"""
    INSERT INTO txs (tx_hash, {columns})
    VALUES (?, {placeholders})
    ON CONFLICT(tx_hash) DO UPDATE SET {update_placeholders};
    """

    # Execute the query
    cursor.execute(query, [tx_hash] + list(record2write.values()) + list(record2write.values()))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def fetch_transactions(address, api_key,startblock, page=1, offset=10):
    base_url = "https://api.etherscan.io/api"

    while True:
        params = {
            'module': 'account',
            'action': 'txlist',
            'address': address,
            'startblock': startblock,
            'endblock': 19164987,
            'page': page,
            'offset': offset,
            'sort': 'asc',
            'apikey': api_key
        }

        response = requests.get(base_url, params=params)
        data = response.json()

        if data['status'] != '1':
            break

        for tx in data['result']:
            calldata=tx['input']
            if tx['methodId'] !='0x3f62192e':
                continue
            if tx['isError'] == 1:
                continue
            maker_address,input_asset,output_asset,recipient_address = parseCalldata.decode4all(calldata)
            if output_asset!='MULTIPLE':
                internal_tx = False
                tx = fetch_tx(tx['hash'])
                record2write = {
                    'tx_hash':tx['hash'],
                    'block_no':int(tx['blockNumber']),
                    'maker_address':maker_address,
                    'input_asset': input_asset,
                    'output_asset': output_asset,
                    'recipient_address':recipient_address,
                    'solver_gas':int(tx['gasPrice'],16)

                }

                if record2write['output_asset'] == '0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee':
                    record2write['output_asset'] = '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2'
                    internal_tx = True

                if record2write['output_asset'] == '0x0000000000000000000000000000000000000000':
                    record2write['output_asset'] = '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2'
                    internal_tx = True
                    
                if record2write['input_asset']  in [PEPE,WETH] and record2write['output_asset']  in [PEPE,WETH]:
                    #has usdc and weth, proceed to fetch token data & reserve data & block time data
                    recipient_address = record2write['recipient_address']
                    if recipient_address =='0x0000000000000000000000000000000000000000':
                        recipient_address = record2write['maker_address'] 

                    logs = fetch_tx_receipt(record2write['tx_hash'])
                    taker_address = parseCalldata.get_taker_address(logs)
                    record2write['taker_address']= taker_address

                    txtally = calcExecution.tally_token_transfer(logs)
                    if txtally != {}:
                        record2write['input_amount'] = hex(-1*txtally[recipient_address][record2write['input_asset']])
                        if internal_tx == False:
                            record2write['output_amount'] = hex(txtally[recipient_address][record2write['output_asset']])
                        else:
                            record2write['output_amount'] = hex(parseCalldata.findETHtransferred(tx['hash'],recipient_address,credentials))
                        univ2_info = fetch_univ2_status(record2write['block_no'])
                        _reserve0,_reserve1 = calcExecution.decode_univ2_info(univ2_info)
                        record2write['reserve0'] =_reserve0
                        record2write['reserve1'] =_reserve1

                        gas_info,amm_gas = fetch_block_gas_info(record2write['block_no'])
                        record2write['med_gas'] =np.median(gas_info)#*0.000000001
                        record2write['max_gas'] =np.max(gas_info)#*0.000000001
                        record2write['min_gas'] =np.min(gas_info)#*0.000000001
                        record2write['amm_gas'] =amm_gas
                        record2write['venue']='UNIX'
                        print(record2write)
                        # collection.update_one({'tx_hash': tx['hash']}, {'$set': record2write}, upsert=True)
            else:
                record2write = {
                        'tx_hash':tx['hash'],
                        'block_no':int(tx['blockNumber'])
                    }
 
            
        # Break if less than 'offset' transactions are returned, indicating last page
        if len(data['result']) < offset:
            break

        page += 1

def get_max_block_number(db_path):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Define the SQL query to get the maximum block number for the specified venue
    query = """
    SELECT MAX(block_no) 
    FROM txs 
    WHERE venue = 'UNIX';
    """

    # Execute the query
    cursor.execute(query)
    result = cursor.fetchone()

    # Close the connection
    conn.close()

    # Check if a result was found and return the maximum block number, or a default value if no record matches the filter
    return int(result[0]) if result[0] is not None else 18000021

# Example usage:
db_path = 'pepe.db'  # Path to your SQLite database
max_block_number = get_max_block_number(db_path)
print(f"Max block number: {max_block_number}")

def fetch_trade_by_tx(tx_hash):
    record2write={}
    tx = fetch_tx(tx_hash)
    calldata=tx['input']
    maker_address,input_asset,output_asset,recipient_address = parseCalldata.decode4all(calldata)
    if output_asset!='MULTIPLE':
        internal_tx = False
        tx = fetch_tx(tx_hash)
        record2write = {
            'tx_hash':tx['hash'],
            'block_no':int(tx['blockNumber'],16),
            'maker_address':maker_address,
            'input_asset': input_asset,
            'output_asset': output_asset,
            'recipient_address':recipient_address,
            'solver_gas':int(tx['gasPrice'],16)

        }

        if record2write['output_asset'] == '0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee':
            record2write['output_asset'] = '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2'
            internal_tx = True

        if record2write['output_asset'] == '0x0000000000000000000000000000000000000000':
            record2write['output_asset'] = '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2'
            internal_tx = True
            
        #has usdc and weth, proceed to fetch token data & reserve data & block time data
        recipient_address = record2write['recipient_address']
        if recipient_address =='0x0000000000000000000000000000000000000000':
            recipient_address = record2write['maker_address'] 

        logs = fetch_tx_receipt(record2write['tx_hash'])
        taker_address = parseCalldata.get_taker_address(logs)
        record2write['taker_address']= taker_address

        txtally = calcExecution.tally_token_transfer(logs)
        if txtally != {}:
            record2write['input_amount'] = hex(-1*txtally[recipient_address][record2write['input_asset']])
            if internal_tx == False:
                record2write['output_amount'] = hex(txtally[recipient_address][record2write['output_asset']])
            else:
                record2write['output_amount'] = hex(parseCalldata.findETHtransferred(tx['hash'],recipient_address,credentials))
            univ2_info = fetch_univ2_status(record2write['block_no'])
            _reserve0,_reserve1 = calcExecution.decode_univ2_info(univ2_info)
            record2write['reserve0'] =_reserve0
            record2write['reserve1'] =_reserve1

            gas_info,amm_gas = fetch_block_gas_info(record2write['block_no'])
            record2write['med_gas'] =np.median(gas_info)#*0.000000001
            record2write['max_gas'] =int(np.max(gas_info))#*0.000000001
            record2write['min_gas'] =int(np.min(gas_info))#*0.000000001
            record2write['amm_gas'] =amm_gas
            record2write['venue']='UNIX'
            print(record2write)
            upsert_record(db_path, record2write['tx_hash'], record2write)
    else:
        record2write = {
                'tx_hash':tx['hash'],
                'block_no':int(tx['blockNumber'])
            }
def main():
    api_key = credentials.get('ETHERSCAN_APIKEY')
    address = '0x6000da47483062A0D734Ba3dc7576Ce6A0B645C4'
    startblock = get_max_block_number(collection) - 1
    fetch_transactions(address, api_key, startblock)

def get_empty_txs():
    conn = sqlite3.connect("pepe.db")
    cursor = conn.cursor()
    sql = '''SELECT tx_hash FROM txs WHERE venue = "UNIX" and input_amount is NULL'''
    cursor.execute(sql)
    tx_hashes=cursor.fetchall()
    random.shuffle(tx_hashes)

    remaining_count = len(tx_hashes)
    for tx_hash in tx_hashes:
        fetch_trade_by_tx(tx_hash[0])
        print(remaining_count, "left")
        remaining_count-=1
    conn.close()

if __name__ == "__main__":
    while 1:
        try:
            # main()
            get_empty_txs()
        except Exception as e:
            print(f"An error occurred: {e}")
    # get_empty_txs()
