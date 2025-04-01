import requests
import json
import time
# Load credentials from file
with open('.credentials', 'r') as file:
    credentials = json.load(file)
import sqlite3
import pandas as pd 
alchemy_api = credentials.get('ALCHEMY_APIKEY')

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

def fetch_gas_from_block(txs):
    for tx in txs:
        if tx['to'] in dex_router_list:
            return (int(tx['gasPrice'],16))
    return "Error"

def fetch_gas_from_tx(txs,tx_hash):
    for tx in txs:
        if tx['hash'] == tx_hash:
            return (int(tx['gasPrice'],16)) 

def fetch(block_no,df):
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
    txs = response['result']['transactions']
    print (block_no)
    tx_hash = df[df['block_no'] == block_no]['tx_hash'].iloc[0]
    solver_gas = fetch_gas_from_tx(txs,tx_hash)
    
    return solver_gas

def fetch_gas_unit_info():
    conn = sqlite3.connect('gdb.db')
    df = pd.read_csv('rawdata.csv')
    # Create a cursor object
    cur = conn.cursor()
    # Fetch records where min_gas is NULL
    cur.execute("SELECT block_no FROM gas WHERE solver_gas IS  NULL")
    rows = cur.fetchall()

    for row in rows:
        block_no = row[0]
        try:
            solver_gas = fetch(block_no,df)
            cur.execute("UPDATE gas SET solver_gas = ? WHERE block_no = ?", (solver_gas, block_no))
            conn.commit()
            print("written",solver_gas,block_no)

        except Exception as e:

            print(f"An error occurred while updating block_no {block_no}: {e}")

fetch_gas_unit_info()