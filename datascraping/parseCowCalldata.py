import json
import requests
import time

def get_taker_address(log_emission):
    for log in log_emission:
        if log['topics'][0] =='0x40338ce1a7c49204f0099533b1e9a7ee0a3d261f84974ab7af36105b8c4e9db4':
            return '0x'+log['topics'][1][26:66].lower()

def decode4all(orderID, max_retries=3, delay=5, timeout=10):
    print(orderID)
    url = f'https://api.cow.fi/mainnet/api/v1/orders/{orderID}'
    attempts = 0

    while attempts < max_retries:
        try:
            response = requests.get(url, timeout=timeout)
            print(url)
            if response.status_code == 200:
                # Parse JSON data from the response
                data = response.json()

                if 'onchainUser' in data.keys():
                    maker_address = data['onchainUser'].lower()
                else:
                    maker_address = data['owner'].lower()
                if data['receiver']!= None:
                    recipient_address = data['receiver'].lower()
                else:
                    recipient_address = maker_address
                input_asset = data['sellToken'].lower()
                output_asset = data['buyToken'].lower()
                if input_asset == '0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee':
                    input_asset = '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2'
                if output_asset == '0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee':
                    output_asset = '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2'
                if input_asset == '0x0000000000000000000000000000000000000000':
                    input_asset = '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2'
                if output_asset == '0x0000000000000000000000000000000000000000':
                    output_asset = '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2'
                output_amount = hex(int(data['executedBuyAmount']))
                input_amount = hex(int(data['executedSellAmount']))
                return maker_address,input_asset,output_asset,recipient_address, output_amount, input_amount
            elif response.status_code == 404:
                break
            else:
                print(f"Attempt {attempts + 1} failed with status code: {response.status_code}. Retrying...")
                attempts += 1
                time.sleep(delay)

        except requests.exceptions.Timeout:
            print(f"Attempt {attempts + 1} timed out after {timeout} seconds. Retrying...")
            attempts += 1
            time.sleep(delay)
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            break

    print(f"Failed to fetch data. Status code: {response.status_code}")
    return None
