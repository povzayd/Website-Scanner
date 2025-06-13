import re
import requests
from bs4 import BeautifulSoup

def scan(url):
    findings = []
    try:
        res = requests.get(url, timeout=5)
        soup = BeautifulSoup(res.text, "html.parser")
        scripts = [tag['src'] for tag in soup.find_all("script") if tag.get("src")]
        for script_url in scripts:
            if not script_url.startswith("http"):
                script_url = url.rstrip("/") + "/" + script_url.lstrip("/")
            try:
                js_content = requests.get(script_url, timeout=5).text
                if re.search(r'(AKIA[0-9A-Z]{16})', js_content) or "api_key" in js_content or "TODO" in js_content:
                    findings.append({
                        "type": "JS Leak",
                        "url": script_url,
                        "match": "Potential API key or TODO found"
                    })
            except:
                continue
    except:
        findings.append({
            "type": "Error",
            "message": "Failed to connect while scanning JS files."
        })
    return findings
