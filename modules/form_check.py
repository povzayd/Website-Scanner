import requests
from bs4 import BeautifulSoup

def scan(url):
    findings = []
    try:
        res = requests.get(url, timeout=5)
        soup = BeautifulSoup(res.text, "html.parser")
        forms = soup.find_all("form")
        for form in forms:
            issue = {}
            inputs = form.find_all("input")
            action = form.get("action", "")
            if not any(i.get("type") == "password" for i in inputs):
                issue["missing_password"] = True
            if action.startswith("http:"):
                issue["insecure_action"] = action
            if not any("csrf" in (i.get("name") or "").lower() for i in inputs):
                issue["missing_csrf"] = True
            if issue:
                issue["type"] = "Form Issue"
                findings.append(issue)
    except:
        findings.append({
            "type": "Error",
            "message": "Failed to connect while analyzing forms."
        })
    return findings
