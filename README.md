# DEX Execution Comparison Dataset

A dataset comparing execution quality across different Decentralized Exchanges (DEXs) and Centralized Exchanges (CEXs), with simulated trade execution analysis. This comprehensive analysis examines transaction costs, price impact, and execution efficiency across trading venues using Tenderly simulation.

The dataset is curated by [Yuki Yuminaga and Dex Chen](https://github.com/username-placeholder), and is part of the [TLDR 2025 fellowship program](https://www.thelatestindefi.org/fellowships).

## About the dataset
*For the entire-range dataset and more details of our work, stay in tune for this repo and the TLDR Conference 2025.*

**size:** 11 MB

**structure:** [25,812 rows, 25 columns]

**source:** CEX data scraping and Tenderly simulation

**blockchain:** Ethereum

**variables:**

| Variable | Type | Description |
| ----------------------- | -------- | ------------------------------------------------------------ |
| `tx_hash` | STRING | Transaction hash identifier |
| `block_no` | INTEGER | Block number of the transaction |
| `venue` | STRING | Trading venue (DEX name) |
| `input_asset` | STRING | Input token address |
| `output_asset` | STRING | Output token address |
| `input_amount` | FLOAT | Amount of input token |
| `output_amount` | FLOAT | Amount of output token received |
| `reserve0` | FLOAT | First token reserve in the liquidity pool |
| `reserve1` | FLOAT | Second token reserve in the liquidity pool |
| `realistic_gas` | FLOAT | Realistic gas cost from GetGas3 |
| `v2_unit` | FLOAT | Tenderly simulated gas for Uniswap V2 |
| `v3_unit` | FLOAT | Tenderly simulated gas for Uniswap V3 |
| `direction` | STRING | Trade direction |
| `eth_volume` | FLOAT | Volume in ETH equivalent |
| `block_timestamp` | FLOAT | Timestamp of the block |
| `closest_BN_price` | FLOAT | Closest Binance price |
| `closest_BN_timestamp` | FLOAT | Timestamp of the closest Binance price |
| `asset` | STRING | Asset being traded |
| `solver_executed_price` | FLOAT | Execution price achieved by the solver, equal to output_amount/input_amount |
| `markout_percentage` | FLOAT | Percentage markout against Binance |
| `net_simulated_v2_output_amount` | FLOAT | Simulated output amount on Uniswap V2 |
| `solver_versus_v2_welfare` | FLOAT | Comparison of solver execution vs Uniswap V2 |
| `log_eth_volume` | FLOAT | Logarithm of ETH volume |
| `net_simulated_v3_output_amount` | FLOAT | Simulated output amount on Uniswap V3 |
| `solver_versus_v3_welfare` | FLOAT | Comparison of solver execution vs Uniswap V3 |

## Implementation Guideline

The various scripts within the datascraping folder of this repository are used to construct the datasets below.

1. **Parsing Scipts**:

   - parseCowCalldata.py, parseUnixCalldata.py, parse1inchCalldata.py
   - These scripts parse the call data of our DEX trades to get the token, volume.

2. **Tenderly Scripts**:

   - newTenderly.py, pepeTenderly.py
   - Tenderly scripts simulate the trade execution and the gas cost.

3. **Calculate Execution Script**:

   - calcExecution.py, getGas3.py
   - Analyzes the logs of the trades to pull information about the swap used in the data, including the from_address, to_address, amount, and the reserve tokens in the swap's pool.
   - The gas script pulls the gas cost for the swap, used for the realistic_gas column.

4. **Main Scripts**:
   - main1inch.py, main1inchMemeLocalDB.py, mainCowMemeLocalDB.py, mainUnix.py, mainUnixMemeLocalDB.py
   - These files call functions from the other scripts to comipile the dataset for trades from 1inch, UniswapX, CowSwap, and for meme tokens. 


Several API keys will be needed to run these scripts, including those from Infura, Alchemy, and Tenderly. The final version of the data used in the paper can be found in this repository and on the TLDR data frontend.
