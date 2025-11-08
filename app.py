# app.py
import os
import sys
import json
import time
import argparse
from typing import Dict, Tuple, Optional
from web3 import Web3

DEFAULT_RPC_SRC = os.environ.get("SRC_RPC_URL", "https://mainnet.infura.io/v3/YOUR_INFURA_KEY")
DEFAULT_RPC_DST = os.environ.get("DST_RPC_URL", "https://arb1.arbitrum.io/rpc")

def get_code_hash(w3: Web3, address: str, block: str = "latest") -> Optional[str]:
    """
    Fetches and returns the keccak hash of a contract's bytecode.
    """
    try:
        address = Web3.to_checksum_address(address)
        code = w3.eth.get_code(address, block_identifier=block)
        if len(code) == 0:
            return None
        return Web3.keccak(code).hex()
    except Exception as e:
        print(f"❌ Error fetching code for {address}: {e}")
        return None

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="bytecode-crosschain-soundness — verify contract bytecode equality across chains (useful for Aztec bridges, Zama rollups, and cross-chain Web3 deployments)."
    )
    p.add_argument("--src-rpc", default=DEFAULT_RPC_SRC, help="Source chain RPC URL (default from SRC_RPC_URL)")
    p.add_argument("--dst-rpc", default=DEFAULT_RPC_DST, help="Destination chain RPC URL (default from DST_RPC_URL)")
    p.add_argument("--address", required=True, help="Contract address to check")
    p.add_argument("--src-block", default="latest", help="Block tag/number on source chain")
    p.add_argument("--dst-block", default="latest", help="Block tag/number on destination chain")
    p.add_argument("--timeout", type=int, default=30, help="RPC timeout seconds (default: 30)")
    p.add_argument("--json", action="store_true", help="Emit results as JSON")
    return p.parse_args()

def main() -> None:
    start = time.time()
    args = parse_args()

    # Validate address format
    if not Web3.is_address(args.address):
        print("❌ Invalid Ethereum address format.")
        sys.exit(1)

    w3_src = Web3(Web3.HTTPProvider(args.src_rpc, request_kwargs={"timeout": args.timeout}))
    w3_dst = Web3(Web3.HTTPProvider(args.dst_rpc, request_kwargs={"timeout": args.timeout}))

    if not w3_src.is_connected():
        print("❌ Source RPC connection failed.")
        sys.exit(1)
    if not w3_dst.is_connected():
        print("❌ Destination RPC connection failed.")
        sys.exit(1)

    print("🔧 bytecode-crosschain-soundness")
    print(f"🌐 Source RPC: {args.src_rpc}")
    print(f"🌐 Destination RPC: {args.dst_rpc}")
    print(f"🏷️ Address: {args.address}")
    print(f"⛓️ Source Block: {args.src_block}")
    print(f"⛓️ Destination Block: {args.dst_block}")

    # Get bytecode hashes
    src_hash = get_code_hash(w3_src, args.address, args.src_block)
    dst_hash = get_code_hash(w3_dst, args.address, args.dst_block)

    if src_hash is None:
        print("❌ Source chain: No code found at this address.")
        sys.exit(2)
    if dst_hash is None:
        print("❌ Destination chain: No code found at this address.")
        sys.exit(2)

    print(f"🔹 Source bytecode hash: {src_hash}")
    print(f"🔸 Destination bytecode hash: {dst_hash}")

    match = src_hash.lower() == dst_hash.lower()
    status = "✅ MATCH" if match else "❌ MISMATCH"
    print(f"🧩 Cross-chain bytecode comparison result: {status}")

    elapsed = time.time() - start
    print(f"⏱️ Completed in {elapsed:.2f}s")

    if args.json:
        result = {
            "address": Web3.to_checksum_address(args.address),
            "src_rpc": args.src_rpc,
            "dst_rpc": args.dst_rpc,
            "src_block": args.src_block,
            "dst_block": args.dst_block,
            "src_hash": src_hash,
            "dst_hash": dst_hash,
            "match": match,
            "elapsed_seconds": round(elapsed, 2),
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))

    sys.exit(0 if match else 2)

if __name__ == "__main__":
    main()
