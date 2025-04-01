import requests
import json
import time
# Load credentials from file
with open('.credentials', 'r') as file:
    credentials = json.load(file)
import sqlite3
import pandas as pd 
import random

# Set your API key here
api_key = credentials['TENDERLY_APIKEY']
simulation_url = ""

def simulateUNIV2sellETH(amountInWei,block_number):
    hex_number = hex(amountInWei)[2:]
    input_amount = hex_number.zfill(64)
    raw_call_data = f'0x38ed1739{input_amount}000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000a0000000000000000000000000f04a1a7b5baf5c7b08ec3be5ff9bdf608e27267c00000000000000000000000000000000000000000000000000000000a1d820de0000000000000000000000000000000000000000000000000000000000000002000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc20000000000000000000000006982508145454Ce325dDbE47a25d4ec3d2311933'
    print(raw_call_data)

    # Simulation payload
    payload = {
        "network_id": "1",  # Adjust according to your target network
        "from": "0xf04a1a7b5baf5c7b08ec3be5ff9bdf608e27267c",
        "to": "0x7a250d5630b4cf539739df2c5dacb4c659f2488d",
        "input": raw_call_data,
        "value": "0",
        "block_number":block_number,
        "simulation_type":"quick",
          "state_objects": {

        '0x6982508145454Ce325dDbE47a25d4ec3d2311933': {
            "storage": {
              '0x39ab9012f260e5672db0f04b3628e133984222d105512611387c33f5d1df6d40':
                '0x00000000000000000000000000000000000014bdda612d4732c54bb0fb04b5d8',
                '0xac3007243a62ea5903d064233f7e08676031d78d583bfb04584946e03373b6f4':
                '0x00000000000000000000000000000000000014bdda612d4732c54bb0fb04b5d8'
            },
          },
        '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2': {
            "storage": {
              '0xa2a3b7f79723c71873b04a732a894ecc62c819fad12fe026d031ce446c4efa80':
                '0x0000000000000000000000000000000000000000006359b65258eea437f80000',
                '0xe6fe701352f539039275882a646e0a9fed5ee2ebd1b3b2cf4390abcab957ca87':
                '0x0000000000000000000000000000000000000000006359b65258eea437f80000'
            },
          }

  }
    }

    # Headers with the API key
    headers = {
        'Content-Type': 'application/json',
        'x-access-key': api_key
    }

    # Sending the POST request
    response = requests.post(simulation_url, json=payload, headers=headers)
    # print(response.json())
    if response.json()['simulation']['status']==True:
        print(response.json()['simulation']['gas_used'])
        return response.json()['simulation']['gas_used']
    else:
        return "Error"

def simulateUNIV2sellUSDC(amountRAWUSDC,block_number):
    hex_number = hex(amountRAWUSDC)[2:]
    input_amount = hex_number.zfill(64)
    raw_call_data = f'0x38ed1739{input_amount}000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000a0000000000000000000000000f04a1a7b5baf5c7b08ec3be5ff9bdf608e27267c00000000000000000000000000000000000000000000000000000000a1d820de00000000000000000000000000000000000000000000000000000000000000020000000000000000000000006982508145454Ce325dDbE47a25d4ec3d2311933000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc2'
    print(raw_call_data)

    # Simulation payload
    payload = {
        "network_id": "1",  # Adjust according to your target network
        "from": "0xf04a1a7b5baf5c7b08ec3be5ff9bdf608e27267c",
        "to": "0x7a250d5630b4cf539739df2c5dacb4c659f2488d",
        "input": raw_call_data,
        "value": "0",
        "block_number":block_number,
        "simulation_type":"quick",
          "state_objects": {
  '0x6982508145454Ce325dDbE47a25d4ec3d2311933': {
            "storage": {
              '0x39ab9012f260e5672db0f04b3628e133984222d105512611387c33f5d1df6d40':
                '0x00000000000000000000000000000000000014bdda612d4732c54bb0fb04b5d8',
                '0xac3007243a62ea5903d064233f7e08676031d78d583bfb04584946e03373b6f4':
                '0x00000000000000000000000000000000000014bdda612d4732c54bb0fb04b5d8'
            },
          },
        '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2': {
            "storage": {
              '0xa2a3b7f79723c71873b04a732a894ecc62c819fad12fe026d031ce446c4efa80':
                '0x0000000000000000000000000000000000000000006359b65258eea437f80000',
                '0xe6fe701352f539039275882a646e0a9fed5ee2ebd1b3b2cf4390abcab957ca87':
                '0x0000000000000000000000000000000000000000006359b65258eea437f80000'
            },
          }

  }
    }

    # Headers with the API key
    headers = {
        'Content-Type': 'application/json',
        'x-access-key': api_key
    }

    # Sending the POST request
    response = requests.post(simulation_url, json=payload, headers=headers)
    # print(response.json())

    if response.json()['simulation']['status']==True:
        print(response.json()['simulation']['gas_used'])
        return response.json()['simulation']['gas_used']
    else:
        return "Error"



def simulateUNIV3sellETH(amountInWei,block_number):
    hex_number = hex(amountInWei)[2:]
    input_amount = hex_number.zfill(64)
    raw_call_data = f'0x04e45aaf000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc20000000000000000000000006982508145454Ce325dDbE47a25d4ec3d231193300000000000000000000000000000000000000000000000000000000000001f4000000000000000000000000f04a1a7b5baf5c7b08ec3be5ff9bdf608e27267c{input_amount}00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
    print(raw_call_data)

    # Simulation payload
    payload = {
        "network_id": "1",  # Adjust according to your target network
        "from": "0xf04a1a7b5baf5c7b08ec3be5ff9bdf608e27267c",
        "to": "0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45",
        "input": raw_call_data,
        "value": "0",
        "block_number":block_number,
        "simulation_type":"quick",
          "state_objects": {
'0x6982508145454Ce325dDbE47a25d4ec3d2311933': {
            "storage": {
              '0x39ab9012f260e5672db0f04b3628e133984222d105512611387c33f5d1df6d40':
                '0x00000000000000000000000000000000000014bdda612d4732c54bb0fb04b5d8',
                '0x9f46e2af4f05b776368809b3e977a81394bbd39d4b78e5961fe69edc1e10ca18':
                '0x00000000000000000000000000000000000014bdda612d4732c54bb0fb04b5d8'
            },
          },
        '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2': {
            "storage": {
              '0x7772b5a1243ab6e8e785239fc581b3ca3542dbd7912f16040dfeb9a8dd4d1d74':
                '0x0000000000000000000000000000000000000000006359b65258eea437f80000',
                '0xe6fe701352f539039275882a646e0a9fed5ee2ebd1b3b2cf4390abcab957ca87':
                '0x0000000000000000000000000000000000000000006359b65258eea437f80000'
            },
          }

  }
    }

    # Headers with the API key
    headers = {
        'Content-Type': 'application/json',
        'x-access-key': api_key
    }

    # Sending the POST request
    response = requests.post(simulation_url, json=payload, headers=headers)
    # print(response.json())

    if response.json()['simulation']['status']==True:
        print(response.json()['simulation']['gas_used'])
        return response.json()['simulation']['gas_used']
    else:
        return "Error"



def simulateUNIV3sellUSDC(amountInWei,block_number):
    hex_number = hex(amountInWei)[2:]
    input_amount = hex_number.zfill(64)
    raw_call_data = f'0x04e45aaf0000000000000000000000006982508145454Ce325dDbE47a25d4ec3d2311933000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc200000000000000000000000000000000000000000000000000000000000001f4000000000000000000000000f04a1a7b5baf5c7b08ec3be5ff9bdf608e27267c{input_amount}00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
    print(raw_call_data)

    # Simulation payload
    payload = {
        "network_id": "1",  # Adjust according to your target network
        "from": "0xf04a1a7b5baf5c7b08ec3be5ff9bdf608e27267c",
        "to": "0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45",
        "input": raw_call_data,
        "value": "0",
        "block_number":block_number,
        "simulation_type":"quick",
          "state_objects": {

        '0x6982508145454Ce325dDbE47a25d4ec3d2311933': {
            "storage": {
              '0x39ab9012f260e5672db0f04b3628e133984222d105512611387c33f5d1df6d40':
                '0x00000000000000000000000000000000000014bdda612d4732c54bb0fb04b5d8',
                '0x9f46e2af4f05b776368809b3e977a81394bbd39d4b78e5961fe69edc1e10ca18':
                '0x00000000000000000000000000000000000014bdda612d4732c54bb0fb04b5d8'
            },
          },
        '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2': {
            "storage": {
              '0x7772b5a1243ab6e8e785239fc581b3ca3542dbd7912f16040dfeb9a8dd4d1d74':
                '0x0000000000000000000000000000000000000000006359b65258eea437f80000',
                '0xe6fe701352f539039275882a646e0a9fed5ee2ebd1b3b2cf4390abcab957ca87':
                '0x0000000000000000000000000000000000000000006359b65258eea437f80000'
            },
          }

  }
    }

    # Headers with the API key
    headers = {
        'Content-Type': 'application/json',
        'x-access-key': api_key
    }

    # Sending the POST request
    response = requests.post(simulation_url, json=payload, headers=headers)
    print(response.json())

    if response.json()['simulation']['status']==True:
        print(response.json()['simulation']['gas_used'])
        return response.json()['simulation']['gas_used']
    else:
        return "Error"
    
def fetch_gas_unit_info():
    conn = sqlite3.connect('pepe.db')

    # Create a cursor object
    cur = conn.cursor()
    # Fetch records where min_gas is NULL
    cur.execute("SELECT tx_hash, block_no,input_asset,input_amount FROM txs WHERE v2_unit IS NULL and input_amount IS NOT NULL and output_amount IS NOT NULL")
    rows = cur.fetchall()
    random.shuffle(rows)

    starting_count = len(rows)
    for row in rows:
        tx_hash, block_no,asset_in,amount_in = row
        print(tx_hash, block_no,asset_in,amount_in)
        if asset_in == "0x6982508145454ce325ddbe47a25d4ec3d2311933":
            amount_in=int(amount_in,16)
            v2_unit = simulateUNIV2sellUSDC(amount_in,block_no)
            if v2_unit == "Error": v2_unit = None
            v3_unit = simulateUNIV3sellUSDC(amount_in,block_no)
            if v3_unit == "Error": v3_unit = None
        else:
            amount_in=int(amount_in,16)
            v2_unit = simulateUNIV2sellETH(amount_in,block_no)
            if v2_unit == "Error": v2_unit = None
            v3_unit = simulateUNIV3sellETH(amount_in,block_no)
            if v3_unit == "Error": v3_unit = None       
        try:
            cur.execute("UPDATE txs SET v2_unit = ? WHERE tx_hash = ?", (v2_unit, tx_hash))
        except sqlite3.Error as e:
            print(f"An error occurred while updating block_no {block_no}: {e}")
        try:
            cur.execute("UPDATE txs SET v3_unit = ? WHERE tx_hash = ?", (v3_unit, tx_hash))
        except sqlite3.Error as e:
            print(f"An error occurred while updating block_no {block_no}: {e}")
        conn.commit()
        starting_count-=1
        print(starting_count," record left")



    # Close the connection
    conn.close()
# simulateUNIV2sellETH(1500000000000000000,19830976)
# simulateUNIV2sellUSDC(1500000000000000000,19830976)
# simulateUNIV3sellETH(1500000000000000000,19830976)
# simulateUNIV3sellUSDC(1500000000000000,19830976)


#fill_unit_table()
while 1:
    try:
      fetch_gas_unit_info()
    except Exception as e:
        print(f"An error occurred: {e}")