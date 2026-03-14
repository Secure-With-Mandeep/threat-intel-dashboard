from correlator import correlate_ip
from datetime import datetime
import json
import os

WATCHLIST_FILE = "watchlist.txt"
ALERTS_FILE = "reports/alerts.json"


def load_watchlist():
    """Load IPs from watchlist.txt"""
    if not os.path.exists(WATCHLIST_FILE):
        print("⚠ No watchlist.txt found!")
        return []

    with open(WATCHLIST_FILE, "r") as f:
        ips = [line.strip() for line in f if line.strip()]

    print(f"📋 Loaded {len(ips)} IPs from watchlist")
    return ips


def save_alert(alert):
    """Save alert to reports/alerts.json"""
    alerts = load_existing_alerts()
    alerts.append(alert)

    with open(ALERTS_FILE, "w") as f:
        json.dump(alerts, f, indent=2)


def load_existing_alerts():
    """Load existing alerts from file"""
    if not os.path.exists(ALERTS_FILE):
        return []

    with open(ALERTS_FILE, "r") as f:
        return json.load(f)


def run_watchlist_scan():
    """Scan all IPs in watchlist and alert on threats"""
    print("\n" + "=" * 50)
    print("🔍 RUNNING WATCHLIST SCAN")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

    ips = load_watchlist()
    if not ips:
        return []

    new_alerts = []

    for ip in ips:
        results = correlate_ip(ip)
        verdict = results["verdict"]

        # Only alert on suspicious or malicious
        if results["threat_score"] >= 3:
            alert = {
                "ip": ip,
                "verdict": verdict,
                "threat_score": results["threat_score"],
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "feeds": results["feeds"]
            }

            new_alerts.append(alert)
            save_alert(alert)

            print(f"\n🚨 ALERT TRIGGERED!")
            print(f"   IP       : {ip}")
            print(f"   Verdict  : {verdict}")
            print(f"   Score    : {results['threat_score']}/9")
            print(f"   Time     : {alert['timestamp']}")
        else:
            print(f"\n✅ {ip} — CLEAN (Score: {results['threat_score']}/9)")

    print("\n" + "=" * 50)
    print(f"✅ Scan complete — {len(new_alerts)} alert(s) triggered")
    print("=" * 50 + "\n")

    return new_alerts


if __name__ == "__main__":
    run_watchlist_scan()
