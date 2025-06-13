import requests

def scan(url):
    findings = []
    dirs = ["/admin/", "/backup/", "/test/", "/uploads/", "/old/"]
    for d in dirs:
        try:
            full_url = url.rstrip("/") + d
            res = requests.get(full_url, timeout=5)
            if "Index of" in res.text and res.status_code == 200:
                findings.append({
                    "type": "Open Directory",
                    "url": full_url
                })
        except:
            continue
    return findings
