from flask import Flask, render_template, request
from correlator import correlate_ip

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

    return render_template("index.html", results=results, error=error)


if __name__ == "__main__":
    app.run(debug=True)
