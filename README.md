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
| `input_asset` | STRING | Input token symbol |
| `output_asset` | STRING | Output token symbol |
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

The data pipeline for this paper implements a multi-step process:

1. **Data Collection**:
   - Scripts scrape CEX and DEX data
   - Parse call data to extract token volumes
   - Move data to local databases

2. **Simulation & Analysis**:
   - Tenderly scripts simulate transaction gas costs
   - Calculate execution simulations and MM output amounts
   - Fetch gas prices for each block where swaps occur
   - Compute mean gas price and standard deviation

3. **Welfare Metrics**:
   - Solver executed price calculation (output/input ratios)
   - Markout percentage against Binance prices
   - Welfare comparison between solver execution and simulated V2/V3 trades


