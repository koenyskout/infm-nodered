import random
import time

import requests

URL = "http://node-red:1880/devices/123"

temperature = 20.0
while True:
    temperature = round(temperature + random.uniform(-3.0, 3.0), 1)
    try:
        r = requests.post(URL, data=str(temperature), timeout=5)
        r.raise_for_status()
        print(f"Sent {temperature}°C (HTTP {r.status_code})", flush=True)
    except requests.RequestException as e:
        print(f"Failed to send: {e}", flush=True)
    time.sleep(2)
