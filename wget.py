import sys
import requests


url = sys.argv[1]
try:
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
except requests.Timeout:
    print("timeout: ", url)
except requests.HTTPError as err:
    print(f"error url={url}, code={err.response.status_code}")
except requests.RequestException:
    print("error")
else:
    print(resp.content)
