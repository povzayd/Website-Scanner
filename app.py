'''''
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import json

app = Flask(__name__, static_folder='output', template_folder='templates')

# Ensure the output directory exists
os.makedirs('output', exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    url = request.form.get('url')

    # 🚨 Fake scan logic – replace with real tool later
    fake_result = {
        "url": url,
        "vulnerabilities": [
            {
                "type": "Reflected XSS",
                "param": "q",
                "payload": "<script>alert(1)</script>"
            },
            {
                "type": "Missing Header",
                "header": "X-XSS-Protection"
            }
        ],
        "status": "Scan Complete"
    }

    # Save the result as JSON
    with open('output/scan_report.json', 'w') as f:
        json.dump(fake_result, f, indent=2)

    return redirect(url_for('report'))

@app.route('/report')
def report():
    try:
        with open('output/scan_report.json') as f:
            report_data = json.load(f)
        return render_template('output/report.html', data=report_data)
    except Exception as e:
        return f"<h1 style='color:red;'>Error loading report:</h1><pre>{e}</pre>"

@app.route('/output/<path:filename>')
def serve_output(filename):
    return send_from_directory('output', filename)

if __name__ == '__main__':
    app.run(debug=True)
''
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import json

# Import your modular scanner logic
from scanner import scan_url

app = Flask(__name__, static_folder='output', template_folder='templates')

# Ensure output directory exists
os.makedirs('output', exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    url = request.form.get('url')

    if not url:
        return "Error: No URL provided."

    try:
        # 🧠 Use real scanning logic from scanner.py
        result = scan_url(url)

        # Save scan result to output JSON file
        with open('output/scan_report.json', 'w') as f:
            json.dump(result, f, indent=2)

        return redirect(url_for('report'))

    except Exception as e:
        return f"<h1 style='color:red;'>Scanner Error</h1><pre>{e}</pre>"

@app.route('/report')
def report():
    try:
        with open('output/scan_report.json') as f:
            report_data = json.load(f)
        return render_template('output/report.html', data=report_data)
    except Exception as e:
        return f"<h1 style='color:red;'>Error loading report:</h1><pre>{e}</pre>"

@app.route('/output/<path:filename>')
def serve_output(filename):
    return send_from_directory('output', filename)

if __name__ == '__main__':
    app.run(debug=True)


from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import json

from scanner import scan_url

app = Flask(__name__, static_folder='output', template_folder='templates')
os.makedirs('output', exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    url = request.form.get('url')
    if not url:
        return "Error: No URL provided."

    try:
        result = scan_url(url)
        with open('output/scan_report.json', 'w') as f:
            json.dump(result, f, indent=2)
        return redirect(url_for('report'))

    except Exception as e:
        return f"<h1 style='color:red;'>Scanner Error</h1><pre>{e}</pre>"

@app.route('/report')
def report():
    try:
        with open('output/scan_report.json') as f:
            report_data = json.load(f)
        return render_template('output/report.html', data=report_data)
    except Exception as e:
        return f"<h1 style='color:red;'>Error loading report:</h1><pre>{e}</pre>"

@app.route('/output/<path:filename>')
def serve_output(filename):
    return send_from_directory('output', filename)

if __name__ == '__main__':
    app.run(debug=True)

'''
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, make_response
import os
import json
import io
from xhtml2pdf import pisa
from scanner import scan_url

app = Flask(__name__, static_folder='output', template_folder='templates')
os.makedirs('output', exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    url = request.form.get('url')
    if not url:
        return "Error: No URL provided."

    try:
        result = scan_url(url)
        with open('output/scan_report.json', 'w') as f:
            json.dump(result, f, indent=2)
        return redirect(url_for('report'))

    except Exception as e:
        return f"<h1 style='color:red;'>Scanner Error</h1><pre>{e}</pre>"

@app.route('/report')
def report():
    try:
        with open('output/scan_report.json') as f:
            report_data = json.load(f)
        return render_template('output/report.html', data=report_data)
    except Exception as e:
        return f"<h1 style='color:red;'>Error loading report:</h1><pre>{e}</pre>"

@app.route('/download/txt')
def download_txt():
    try:
        with open('output/scan_report.json') as f:
            data = json.load(f)

        txt_output = f"XSS LABS - Scan Report\nTarget: {data['url']}\nStatus: {data['status']}\n\nFindings:\n"

        for vuln in data.get("vulnerabilities", []):
            line = f"- {vuln.get('type')}"
            for key, value in vuln.items():
                if key != "type":
                    line += f" | {key}: {value}"
            txt_output += line + "\n"

        response = make_response(txt_output)
        response.headers["Content-Disposition"] = "attachment; filename=scan_report.txt"
        response.headers["Content-Type"] = "text/plain"
        return response

    except Exception as e:
        return f"Error generating TXT: {e}"

@app.route('/download/pdf')
def download_pdf():
    try:
        with open('output/scan_report.json') as f:
            data = json.load(f)

        html = f"""
        <html>
        <head><style>body {{ font-family: monospace; }}</style></head>
        <body>
        <h2>XSS LABS - PDF Report</h2>
        <p><strong>Target:</strong> {data['url']}</p>
        <p><strong>Status:</strong> {data['status']}</p>
        <h3>Findings:</h3>
        <ul>
        """

        for vuln in data.get("vulnerabilities", []):
            html += "<li><strong>{}</strong>".format(vuln.get("type", ""))
            for key, value in vuln.items():
                if key != "type":
                    html += f"<br><code>{key}:</code> {value}"
            html += "</li><br>"

        html += "</ul></body></html>"

        pdf = io.BytesIO()
        pisa_status = pisa.CreatePDF(html, dest=pdf)

        if pisa_status.err:
            return "Failed to generate PDF"

        pdf.seek(0)
        response = make_response(pdf.read())
        response.headers['Content-Disposition'] = 'attachment; filename=scan_report.pdf'
        response.headers['Content-Type'] = 'application/pdf'
        return response

    except Exception as e:
        return f"Error generating PDF: {e}"

@app.route('/output/<path:filename>')
def serve_output(filename):
    return send_from_directory('output', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

