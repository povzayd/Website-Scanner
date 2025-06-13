import requests

def scan(url):
    findings = []
    try:
        res = requests.get(url, timeout=5)
        if "X-Frame-Options" not in res.headers and "Content-Security-Policy" not in res.headers:
            findings.append({
                "type": "Clickjacking",
                "description": "Missing X-Frame-Options and CSP headers"
            })
    except:
        findings.append({
            "type": "Error",
            "message": "Failed to connect while checking for clickjacking."
        })
    return findings
