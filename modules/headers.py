import requests

def scan(url):
    findings = []
    try:
        res = requests.get(url, timeout=5)
        headers = res.headers
        for header in [
            "Strict-Transport-Security",
            "X-Frame-Options",
            "Content-Security-Policy",
            "X-Content-Type-Options",
            "Referrer-Policy"
        ]:
            if header not in headers:
                findings.append({
                    "type": "Missing Header",
                    "header": header
                })
    except:
        findings.append({
            "type": "Error",
            "message": "Failed to connect while checking headers."
        })
    return findings

