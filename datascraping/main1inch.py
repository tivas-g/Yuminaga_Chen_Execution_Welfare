from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import json
import parse1inchCalldata as parseCalldata
import calcExecution
import numpy as np

with open('.credentials', 'r') as file:
    credentials = json.load(file)

mongodb_password = credentials.get('MONGODB_PASSWORD')
uri = f""
# Create a new MongoDB client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Choose a database and a collection in MongoDB
db = client['rfq-prod']
collection = db['TXS']

alchemy_api = credentials.get('ALCHEMY_APIKEY')
infura_api =  credentials.get('INFURA_APIKEY')

import requests
import time

USDC = '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48'
WETH = '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2'

def fetch_univ2_status(block_no):
    infura_url = f"https://mainnet.infura.io/v3/{infura_api}"

    contract_address = '0xB4e16d0168e52d35CaCD2c6185b44281Ec28C9Dc'

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
    
    gas_price_array=[]
    for tx in response['result']['transactions']:
        gas_price_array.append((int(tx['gasPrice'],16)))
    
    return gas_price_array

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


def fetch_transactions(address, api_key,startblock, page=1, offset=10):
    base_url = "https://api.etherscan.io/api"

    while True:
        params = {
            'module': 'account',
            'action': 'txlist',
            'address': address,
            'startblock': startblock,
            'endblock': 99999999,
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
            if tx['methodId'] !='0x0965d04b':
                continue
            if tx['isError'] == 1:
                continue
            record2write = {
                'tx_hash':tx['hash'],
                'block_no':int(tx['blockNumber']),
                'maker_address':parseCalldata.decode4makeraddress(calldata),
                'input_asset': parseCalldata.decode4inputassetaddress(calldata),
                'output_asset': parseCalldata.decode4outputassetaddress(calldata),
                'taker_address': parseCalldata.decode4takeraddress(calldata),
                'input_amount': parseCalldata.decode4inputamount(calldata),
                'recipient_address':parseCalldata.decode4receipientaddress(calldata)
            }
            if record2write['recipient_address'] =='0x0000000000000000000000000000000000000000':
                record2write['recipient_address'] = record2write['maker_address'] 
            if record2write['input_asset']  in [USDC,WETH] and record2write['output_asset']  in [USDC,WETH]:
                #has usdc and weth, proceed to fetch token data & reserve data & block time data
                recipient_address = record2write['recipient_address']

                logs = fetch_tx_receipt(record2write['tx_hash'])
            
                txtally = calcExecution.tally_token_transfer(logs)
                if txtally != {}:
                    record2write['output_amount'] = hex(txtally[record2write['recipient_address']][record2write['output_asset']])

                    univ2_info = fetch_univ2_status(record2write['block_no'])
                    _reserve0,_reserve1 = calcExecution.decode_univ2_info(univ2_info)
                    record2write['reserve0'] =_reserve0
                    record2write['reserve1'] =_reserve1

                    gas_info = fetch_block_gas_info(record2write['block_no'])
                    record2write['median_gas'] =np.median(gas_info)*0.000000001

            record2write['venue']='1INCH'
            print(record2write)
            collection.update_one({'tx_hash': tx['hash']}, {'$set': record2write}, upsert=True)
            
        # Break if less than 'offset' transactions are returned, indicating last page
        if len(data['result']) < offset:
            break

        page += 1

def get_max_block_number(collection):
    filter = {"venue": "1INCH"}

    # Fetch the maximum block number with the specified filter
    max_block_record = collection.find_one(filter, sort=[("block_no", -1)], projection={"block_no": 1, "_id": 0})
    
    # Check if a record was found and return the maximum block number, or a default value if no record matches the filter
    return int(max_block_record['block_no']) if max_block_record else 16241236


def main():
    api_key = credentials.get('ETHERSCAN_APIKEY')
    address = '0xA88800CD213dA5Ae406ce248380802BD53b47647'
    startblock = get_max_block_number(collection) - 1
    # startblock = 16385266

    fetch_transactions(address, api_key, startblock)

if __name__ == "__main__":
    while 1:
        try:
            main()
        except:
            pass