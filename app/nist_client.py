import requests

def fetch_nist_vulnerabilities():
    url = "https://services.nvd.nist.gov/rest/json/cves/2.0/"
    response = requests.get(url)
    # Procesar y resumir por severidad
    return response.json()