import time
import urllib.request

URL = "http://127.0.0.1:5000"
TIMEOUT = 30
INTERVAL = 1

start_time = time.time()

while time.time() - start_time < TIMEOUT:
    try:
        urllib.request.urlopen(URL, timeout=2)
        print("Application is ready.")
        break

    except Exception:
        print("Application not ready. Retrying...")
        time.sleep(INTERVAL)

else:
    raise RuntimeError(
        f"Application was not ready within {TIMEOUT} seconds."
    )