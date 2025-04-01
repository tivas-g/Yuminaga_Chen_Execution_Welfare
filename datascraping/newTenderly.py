import requests
import json
import time
# Load credentials from file
with open('.credentials', 'r') as file:
    credentials = json.load(file)
import sqlite3
import pandas as pd 
# Set your API key here
api_key = credentials['TENDERLY_APIKEY']
simulation_url = ""

def simulateUNIV2sellETH(amountInWei,block_number):
    hex_number = hex(amountInWei)[2:]
    input_amount = hex_number.zfill(64)
    raw_call_data = f'0x38ed1739{input_amount}000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000a0000000000000000000000000f04a1a7b5baf5c7b08ec3be5ff9bdf608e27267c00000000000000000000000000000000000000000000000000000000a1d820de0000000000000000000000000000000000000000000000000000000000000002000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc2000000000000000000000000a0b86991c6218b36c1d19d4a2e9eb0ce3606eb48'
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

        '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48': {
            "storage": {
              '0x71e983d2870f07f080d4758e05e6cd09d1ec84153f2d81def1c478adbc966b27':
                '0x000000000000000000000000000000000000000000000000232fb9318a12a33c',
                '0xe6ddcc0b25854e6d5cd6fb7932e684b5c85a0c7097476fd5279b60c3ae6f38e9':
                '0x000000000000000000000000000000000000000000000000232fb9318a12a33c'
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
    if response.json()['simulation']['status']==True:
        print(response.json()['simulation']['gas_used'])
        return response.json()['simulation']['gas_used']
    else:
        return "Error"

def simulateUNIV2sellUSDC(amountRAWUSDC,block_number):
    hex_number = hex(amountRAWUSDC)[2:]
    input_amount = hex_number.zfill(64)
    raw_call_data = f'0x38ed1739{input_amount}000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000a0000000000000000000000000f04a1a7b5baf5c7b08ec3be5ff9bdf608e27267c00000000000000000000000000000000000000000000000000000000a1d820de0000000000000000000000000000000000000000000000000000000000000002000000000000000000000000a0b86991c6218b36c1d19d4a2e9eb0ce3606eb48000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc2'
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

        '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48': {
            "storage": {
              '0x71e983d2870f07f080d4758e05e6cd09d1ec84153f2d81def1c478adbc966b27':
                '0x000000000000000000000000000000000000000000000000232fb9318a12a33c',
                '0xe6ddcc0b25854e6d5cd6fb7932e684b5c85a0c7097476fd5279b60c3ae6f38e9':
                '0x000000000000000000000000000000000000000000000000232fb9318a12a33c'
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
    if response.json()['simulation']['status']==True:
        print(response.json()['simulation']['gas_used'])
        return response.json()['simulation']['gas_used']
    else:
        return "Error"



def simulateUNIV3sellETH(amountInWei,block_number):
    hex_number = hex(amountInWei)[2:]
    input_amount = hex_number.zfill(64)
    raw_call_data = f'0x04e45aaf000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc2000000000000000000000000a0b86991c6218b36c1d19d4a2e9eb0ce3606eb4800000000000000000000000000000000000000000000000000000000000001f4000000000000000000000000f04a1a7b5baf5c7b08ec3be5ff9bdf608e27267c{input_amount}00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
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

        '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48': {
            "storage": {
              '0x0bd782be22dd8dfd0e6adc303bc3e6164aa7fafd19b1019820a9e9c2885b9c8c':
                '0x000000000000000000000000000000000000000000000000232fb9318a12a33c',
                '0x71e983d2870f07f080d4758e05e6cd09d1ec84153f2d81def1c478adbc966b27':
                '0x000000000000000000000000000000000000000000000000232fb9318a12a33c'
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
    if response.json()['simulation']['status']==True:
        print(response.json()['simulation']['gas_used'])
        return response.json()['simulation']['gas_used']
    else:
        return "Error"



def simulateUNIV3sellUSDC(amountInWei,block_number):
    hex_number = hex(amountInWei)[2:]
    input_amount = hex_number.zfill(64)
    raw_call_data = f'0x04e45aaf000000000000000000000000a0b86991c6218b36c1d19d4a2e9eb0ce3606eb48000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc200000000000000000000000000000000000000000000000000000000000001f4000000000000000000000000f04a1a7b5baf5c7b08ec3be5ff9bdf608e27267c{input_amount}00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
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

        '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48': {
            "storage": {
              '0x0bd782be22dd8dfd0e6adc303bc3e6164aa7fafd19b1019820a9e9c2885b9c8c':
                '0x000000000000000000000000000000000000000000000000232fb9318a12a33c',
                '0x71e983d2870f07f080d4758e05e6cd09d1ec84153f2d81def1c478adbc966b27':
                '0x000000000000000000000000000000000000000000000000232fb9318a12a33c'
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
    if response.json()['simulation']['status']==True:
        print(response.json()['simulation']['gas_used'])
        return response.json()['simulation']['gas_used']
    else:
        return "Error"


def fill_unit_table():
    import sqlite3

    # Establish a connection to the SQLite database
    # Replace 'your_database.db' with your actual database file
    conn = sqlite3.connect('gdb.db')

    # Create a cursor object
    cur = conn.cursor()
    df = pd.read_csv('rawdata_SimulatedWithUniV3_startat18000000.csv')

    # Iterate through each row
    for index, row in df.iterrows():
        try:
            if row['direction']=="Long":
                asset_in="USDC"
                amount_in=row['input_amount']
            else:
                asset_in="WETH"
                amount_in=row['input_amount']

            cur.execute("INSERT OR IGNORE INTO unit (tx_hash, block_no,asset_in,amount_in ) VALUES (?, ?,?,?)", (row['tx_hash'],row['block_no'],asset_in, amount_in))
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    # Commit the changes to the database
    conn.commit()

    # Close the connection
    conn.close()

    print("Data inserted successfully, duplicates were ignored.")
    
def fetch_gas_unit_info():
    conn = sqlite3.connect('gdb.db')

    # Create a cursor object
    cur = conn.cursor()
    # Fetch records where min_gas is NULL
    cur.execute("SELECT tx_hash, block_no,asset_in,amount_in FROM unit WHERE v2_unit IS NULL")
    rows = cur.fetchall()

    for row in rows:
        tx_hash, block_no,asset_in,amount_in = row
        print(tx_hash, block_no,asset_in,amount_in)
        
        if asset_in == "USDC":
            amount_in=int(amount_in*10**6)
            v2_unit = simulateUNIV2sellUSDC(amount_in,block_no)
            if v2_unit == "Error": v2_unit = None
            v3_unit = simulateUNIV3sellUSDC(amount_in,block_no)
            if v3_unit == "Error": v3_unit = None
        else:
            amount_in=int(amount_in*10**18)
            v2_unit = simulateUNIV2sellETH(amount_in,block_no)
            if v2_unit == "Error": v2_unit = None
            v3_unit = simulateUNIV3sellETH(amount_in,block_no)
            if v3_unit == "Error": v3_unit = None       
        try:
            cur.execute("UPDATE unit SET v2_unit = ? WHERE tx_hash = ?", (v2_unit, tx_hash))
        except sqlite3.Error as e:
            print(f"An error occurred while updating block_no {block_no}: {e}")
        try:
            cur.execute("UPDATE unit SET v3_unit = ? WHERE tx_hash = ?", (v3_unit, tx_hash))
        except sqlite3.Error as e:
            print(f"An error occurred while updating block_no {block_no}: {e}")
        conn.commit()


    # Close the connection
    conn.close()
# simulateUNIV2sellETH(1500000000000000000,19830976)
# simulateUNIV2sellUSDC(15000000,19830976)
# simulateUNIV3sellETH(1500000000000000000,19830976)
# simulateUNIV3sellUSDC(15000000,19830976)


#fill_unit_table()
fetch_gas_unit_info()