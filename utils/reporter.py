
import os
from datetime import datetime

def save_report(data):
    html = "<html><head><title>Scan Report</title></head><body>"
    html += f"<h2>Scan Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</h2><hr>"
    for entry in data:
        html += f"<h3>{entry['url']}</h3><ul>"
        for f in entry['findings']:
            html += f"<li>{f}</li>"
        html += "</ul>"
    html += "</body></html>"

    os.makedirs("output", exist_ok=True)
    with open("output/report.html", "w") as f:
        f.write(html)
    print("\n[+] Report saved to output/report.html")
