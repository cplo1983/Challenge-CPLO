import requests
from collections import defaultdict

def get_nist_summary(exclude_cves=None):
    # Consulta la API de NIST por CVEs
    url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
    params = {"resultsPerPage": 2000}
    r = requests.get(url, params=params)
    data = r.json()
    severities = defaultdict(int)
    for item in data.get("vulnerabilities", []):
        cve_id = item["cve"]["id"]
        if exclude_cves and cve_id in exclude_cves:
            continue
        sev = item["cve"]["metrics"]["cvssMetricV2"][0]["baseSeverity"]
        severities[sev] += 1
    return {"summary": dict(severities)}

def get_cve_by_id(cve_id):
    url = f"https://services.nvd.nist.gov/rest/json/cve/1.0/{cve_id}"
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()
    return None