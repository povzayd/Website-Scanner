#scanner.py
#test 001! working usage python scanner.py url
'''import sys
from modules import open_dir, headers, clickjack, js_leaks, form_check

def run_scanner(url):
    print(f"\n[+] Scanning: {url}\n")
    open_dir.scan(url)
    headers.scan(url)
    clickjack.scan(url)
    js_leaks.scan(url)
    form_check.scan(url)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scanner.py <url>")
        sys.exit(1)
    run_scanner(sys.argv[1])
'
# scanner.py
from modules import open_dir, headers, clickjack, js_leaks, form_check

def scan_url(url):
    results = {
        "url": url,
        "status": "Scan Complete",
        "vulnerabilities": []
    }

    modules = [open_dir, headers, clickjack, js_leaks, form_check]

    for module in modules:
        try:
            findings = module.scan(url)
            if findings:
                results["vulnerabilities"].extend(findings)
        except Exception as e:
            results["vulnerabilities"].append({
                "type": "Module Error",
                "module": module.__name__,
                "error": str(e)
            })

    return results

'''
from modules import open_dir, headers, clickjack, js_leaks, form_check

def scan_url(url):
    results = {
        "url": url,
        "status": "Scan Complete",
        "vulnerabilities": []
    }

    modules = [open_dir, headers, clickjack, js_leaks, form_check]

    for module in modules:
        try:
            findings = module.scan(url)
            if findings:
                results["vulnerabilities"].extend(findings)
        except Exception as e:
            results["vulnerabilities"].append({
                "type": "Module Error",
                "module": module.__name__,
                "error": str(e)
            })

    return results

