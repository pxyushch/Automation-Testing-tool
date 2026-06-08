
import time

def smart_wait_for_selector(page, selector, timeout=5000, retries=3):
    for attempt in range(retries):
        try:
            page.wait_for_selector(selector, timeout=timeout)
            return True
        except Exception:
            time.sleep(0.5)
    return False
