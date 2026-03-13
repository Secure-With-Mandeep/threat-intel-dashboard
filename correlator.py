from feeds.abuseipdb import check_ip as abuseipdb_check
from feeds.virustotal_feed import check_ip as vt_check
from feeds.greynoise_feed import quick_check as gn_check

def correlate_ip(ip_address):
    """
    Query all 3 feeds for an IP and return a unified threat verdict
    """
    print(f"\n🔍 Investigating IP: {ip_address}")
    print("=" * 50)

    results = {
        "ip": ip_address,
        "feeds": {},
        "threat_score": 0,
        "verdict": "CLEAN"
    }

    # --- AbuseIPDB ---
    print("Querying AbuseIPDB...")
    abuse_data = abuseipdb_check(ip_address)
    if abuse_data:
        score = abuse_data.get("abuseConfidenceScore", 0)
        results["feeds"]["abuseipdb"] = {
            "abuse_score": score,
            "total_reports": abuse_data.get("totalReports", 0),
            "country": abuse_data.get("countryCode", "Unknown"),
            "source": "AbuseIPDB"
        }
        # Add to threat score
        if score > 80:
            results["threat_score"] += 3
        elif score > 40:
            results["threat_score"] += 2
        elif score > 10:
            results["threat_score"] += 1

    # --- VirusTotal ---
    print("Querying VirusTotal...")
    vt_data = vt_check(ip_address)
    if vt_data:
        malicious = vt_data.get("malicious_votes", 0)
        results["feeds"]["virustotal"] = {
            "malicious_votes": malicious,
            "suspicious_votes": vt_data.get("suspicious_votes", 0),
            "harmless_votes": vt_data.get("harmless_votes", 0),
            "country": vt_data.get("country", "Unknown"),
            "source": "VirusTotal"
        }
        # Add to threat score
        if malicious > 10:
            results["threat_score"] += 3
        elif malicious > 5:
            results["threat_score"] += 2
        elif malicious > 0:
            results["threat_score"] += 1

    # --- GreyNoise ---
    print("Querying GreyNoise...")
    gn_data = gn_check(ip_address)
    if gn_data:
        classification = gn_data.get("classification", "unknown")
        results["feeds"]["greynoise"] = {
            "classification": classification,
            "noise": gn_data.get("noise", False),
            "riot": gn_data.get("riot", False),
            "source": "GreyNoise"
        }
        # Add to threat score
        if classification == "malicious":
            results["threat_score"] += 3
        elif classification == "suspicious":
            results["threat_score"] += 2

    # --- Final Verdict ---
    if results["threat_score"] >= 6:
        results["verdict"] = "🔴 MALICIOUS"
    elif results["threat_score"] >= 3:
        results["verdict"] = "🟡 SUSPICIOUS"
    else:
        results["verdict"] = "🟢 CLEAN"

    return results


def print_report(results):
    """Print a clean readable report"""
    print("\n" + "=" * 50)
    print(f"📊 THREAT INTELLIGENCE REPORT")
    print("=" * 50)
    print(f"IP Address   : {results['ip']}")
    print(f"Threat Score : {results['threat_score']}/9")
    print(f"Verdict      : {results['verdict']}")
    print("\n--- Feed Results ---")

    for feed_name, data in results["feeds"].items():
        print(f"\n[{data['source']}]")
        for key, value in data.items():
            if key != "source":
                print(f"  {key}: {value}")

    print("\n" + "=" * 50)


if __name__ == "__main__":
    # Test with a known bad IP
    test_ips = [
        "8.8.8.8",        # Google DNS - should be CLEAN
        "185.220.101.1",  # Known Tor exit node - should be SUSPICIOUS/MALICIOUS
    ]

    for ip in test_ips:
        results = correlate_ip(ip)
        print_report(results)
        print("\n")
