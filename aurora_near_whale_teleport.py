import requests, time

def aurora_teleport():
    print("Aurora ↔ NEAR — Whale Teleport Detector (> $3M cross-engine move)")
    seen = set()
    while True:
        # Aurora → NEAR Rainbow Bridge withdrawals
        r = requests.get("https://aurorascan.dev/api?module=account&action=txlist&address=0x23ddd3e3692d1861ed57ede224608875809e127&sort=desc")
        for tx in r.json().get("result", [])[:30]:
            h = tx["hash"]
            if h in seen: continue
            seen.add(h)

            # Rainbow Bridge contract on Aurora side
            if tx["to"].lower() != "0x23ddd3e3692d1861ed57ede224608875809e127": continue
            if "withdraw" not in tx.get("input", "").lower(): continue

            value = int(tx["value"]) / 1e18
            if value >= 3_000_000:  # > $3M in ETH/USDT/etc leaving Aurora → NEAR
                print(f"WHALE TELEPORTED\n"
                      f"${value:,.0f} leaving Aurora → NEAR mainnet\n"
                      f"Wallet: {tx['from']}\n"
                      f"Tx: https://aurorascan.dev/tx/{h}\n"
                      f"→ Money escaping Ethereum L2 back to NEAR\n"
                      f"{'-'*60}")
        time.sleep(3.3)

if __name__ == "__main__":
    aurora_teleport()
