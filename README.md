# bytecode-crosschain-soundness

## Overview
A Python-based CLI tool that verifies **cross-chain soundness** by comparing smart contract bytecode hashes between two EVM-compatible chains.  
This ensures the contract deployed on multiple chains (e.g., **Ethereum** and **Arbitrum**, or **Aztec L1 bridge** and **Zama rollup verifier**) is identical and sound.

## Features
- Compare bytecode between two chains using RPCs  
- Works with any EVM-compatible networks (Ethereum, Arbitrum, Base, Polygon, etc.)  
- Supports specific block numbers or finalized tags  
- JSON output for CI/CD or automated audits  
- Clear emoji-based output for quick visual results  

## Installation
1. Install Python 3.9+  
2. Install dependencies:
   pip install web3
3. Set your RPC URLs (optional):
   export SRC_RPC_URL=https://mainnet.infura.io/v3/YOUR_KEY  
   export DST_RPC_URL=https://arb1.arbitrum.io/rpc

## Usage
Compare contract bytecode between chains:
   python app.py --address 0x00000000219ab540356cBB839Cbe05303d7705Fa

Specify blocks for historical comparison:
   python app.py --address 0xYourContract --src-block 21000000 --dst-block 21000000

Custom RPCs:
   python app.py --src-rpc https://mainnet.infura.io/v3/YOUR_KEY --dst-rpc https://base-mainnet.g.alchemy.com/v2/YOUR_KEY --address 0xYourContract

JSON output for automation:
   python app.py --address 0xYourContract --json

## Example Output
### ❌ Mismatch between source and destination chains
🔧 bytecode-crosschain-soundness  
🌐 Source RPC: https://mainnet.infura.io/v3/YOUR_KEY  
🌐 Destination RPC: https://base-mainnet.g.alchemy.com/v2/YOUR_KEY  
🏷️ Address: 0x1234567890abcdef1234567890abcdef12345678  
⛓️ Source Block: 21000000  
⛓️ Destination Block: 21000000  
🔹 Source bytecode hash: 0x92babcdd4a3e9ff00e761acbe1290eabfbeaa9981a45c1ce48b1f7df89d1cc12  
🔸 Destination bytecode hash: 0x11aa00dd44b33fdd0098229f33ee56ab22fe7781a56c2fcd899b2ee33aa4e892  
🧩 Cross-chain bytecode comparison result: ❌ MISMATCH  
⏱️ Completed in 0.69s  

## Notes
- If either chain returns no code, the tool will exit with code `2` and print an error.  
- Works across all EVM-compatible chains; ideal for cross-chain bridge verifications.  
- You can use this in CI pipelines to ensure deployment consistency between testnet and mainnet.  
- Always pin to specific blocks for deterministic results (especially during rollup reorgs).  
- This tool performs only read operations — it is safe to run against production RPCs.  
- For Aztec/Zama systems, verifying bytecode soundness across chains ensures integrity of rollup verifiers and bridge contracts.  
- Recommended integration: run nightly to detect any unexpected redeployments or upgrades.  
- Exit codes:  
  `0` → soundness verified (match)  
  `2` → mismatch or missing contract code.

