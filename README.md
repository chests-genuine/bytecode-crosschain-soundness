# bytecode-crosschain-soundness

# Overview
This repository contains a tiny CLI tool that compares deployed bytecode hashes for the same contract addresses across two different RPC endpoints or networks. It helps ensure cross-chain or cross-RPC consistency and catches drift after upgrades, re-deploys, or indexing bugs. This is useful for monitoring L1 contracts that coordinate with privacy/zk ecosystems like Aztec or Zama where interface and code soundness is critical.

# What it does
1) Connects to two RPC endpoints (A and B).
2) Fetches runtime bytecode for each target address at user-specified blocks.
3) Computes keccak hashes of bytecode on both sides.
4) Reports per-address MATCH/MISMATCH and provides a JSON summary for CI.

# Installation
1) Requires Python 3.9+.
2) Install dependencies:
   pip install web3
3) Provide two RPC endpoints via flags or environment variables:
   RPC_A_URL and RPC_B_URL

# Usage
Compare a single address:
   python app.py --address 0xYourContract

Compare multiple addresses:
   python app.py --address 0xA --address 0xB --address 0xC

Use a manifest with a list of addresses (JSON array):
   python app.py --manifest ./addresses.json

Set explicit RPCs and blocks:
   python app.py --rpc-a https://mainnet.infura.io/v3/YOUR_KEY --rpc-b https://rpc.ankr.com/eth --block-a finalized --block-b 21000000

Emit JSON for CI:
   python app.py --manifest addresses.json --json --quiet

# Arguments
--rpc-a        RPC URL for chain A (default from RPC_A_URL)
--rpc-b        RPC URL for chain B (default from RPC_B_URL)
--block-a      Block tag or number for chain A (default: finalized)
--block-b      Block tag or number for chain B (default: finalized)
--address      Address to compare; can be repeated multiple times
--manifest     Path to a JSON file containing an array of addresses
--timeout      HTTP timeout in seconds (default: 30)
--concurrency  Number of parallel comparisons (default: 8)
--json         Print machine-readable JSON summary
--quiet, -q    Suppress normal output; print only mismatches and errors

# Manifest format
The manifest file is a JSON array of addresses, for example:
[
  "0x00000000219ab540356cBB839Cbe05303d7705Fa",
  "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
]

# Expected output
You will see a header with RPCs, block tags, and then one line per address:
🔍 0x... -> A:0x...  B:0x... | ✅ MATCH
or
🔍 0x... -> A:0x...  B:0x... | ❌ MISMATCH
Exit code is 0 if all addresses match; 2 if any mismatch or error occurs.

# Notes
- Set blocks to finalized/safe when you need determinism and lower reorg risk.
- If comparing the same chain via two different providers, mismatches can reveal provider indexing issues.
- For proxy architectures, compare the implementation address directly to avoid false mismatches at the proxy layer.
- Relevant for Aztec/Zama deployments where L1 contract soundness and mirror consistency are critical to system integrity.
- This tool checks bytecode equality only; it does not verify ABI, events, or storage layout.
