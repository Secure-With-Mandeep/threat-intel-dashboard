from flask import Flask, render_template, request
from correlator import correlate_ip
from alerts import load_existing_alerts, run_watchlist_scan

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    results = None
    error = None

    if request.method == "POST":
        ip = request.form.get("ip_address", "").strip()
        if ip:
            try:
                results = correlate_ip(ip)
            except Exception as e:
                error = f"Error investigating IP: {str(e)}"
        else:
            error = "Please enter an IP address"

    # Load existing alerts for sidebar
    alerts = load_existing_alerts()

    return render_template(
        "index.html",
        results=results,
        error=error,
        alerts=alerts[-10:]  # Show last 10 alerts
    )


@app.route("/scan", methods=["POST"])
def scan_watchlist():
    """Trigger a watchlist scan"""
    run_watchlist_scan()
    alerts = load_existing_alerts()
    return render_template(
        "index.html",
        results=None,
        error=None,
        alerts=alerts[-10:],
        scan_done=True
    )


if __name__ == "__main__":
    app.run(debug=True)
