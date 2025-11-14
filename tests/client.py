import sys
import time
from dataclasses import dataclass
from typing import List, Optional
import requests


BASE_URL = "http://localhost:8080"
API_PREFIX = "/api"
WAIT_TIMEOUT_SEC = 15.0


@dataclass
class Check:
    name: str
    method: str
    path: str
    expected_status: int
    expected_text_in_body: Optional[str] = None
    expected_json_is_list: bool = False


def make_request(sess: requests.Session, method: str, path: str) -> requests.Response:
    """
    Performs a single request and returns the Response object.
    Raises RuntimeError on connection errors.
    """
    url = BASE_URL.rstrip("/") + path
    method = method.upper()
    try:
        resp = sess.request(method, url, timeout=5)
        return resp
    except requests.RequestException as e:
        raise RuntimeError(f"Request error: {e}") from e


def wait_for_server(sess: requests.Session, timeout_sec: float = WAIT_TIMEOUT_SEC) -> bool:
    """
    Waits for 200 OK on '/'.

    Returns:   True if ready 
               False on timeout
    """

    deadline = time.time() + timeout_sec
    

    while time.time() < deadline:
        try:
            resp = make_request(sess, "GET", "/")
            if resp.status_code == 200:
                print("Server is ready.")
                return True
        except RuntimeError:
            pass
        time.sleep(0.5)
        

    print(f"::error::Server wait timed out after {timeout_sec}s.")
    return False



def run_check(sess: requests.Session, chk: Check) -> Optional[str]:
    """
    Runs a check.

    Returns: None on success
             An error message string on failure
    """

    try:
        resp = make_request(sess, chk.method, chk.path)

        if resp.status_code != chk.expected_status:
            return f"Got status {resp.status_code}, expected {chk.expected_status}"
        
        if chk.expected_text_in_body:
            if chk.expected_text_in_body not in resp.text:
                return f"Did not find text '{chk.expected_text_in_body}' in response"

        if chk.expected_json_is_list:
            try:
                data = resp.json()
                if not isinstance(data, list) or len(data) == 0:
                    return "Response was not a valid, non-empty list"
            except requests.exceptions.JSONDecodeError:
                return "Response was not valid JSON"
        
        return None
        
    except Exception as e:
        return f"Check failed with exception: {e}"


def main() -> int:
    sess = requests.Session()
    sess.headers.update({"Accept": "application/json, text/html"})

    if not wait_for_server(sess):
        return 1

    checks: List[Check] = [
        Check(
            name="UI Check",
            method="GET",
            path="/",
            expected_status=200,
            expected_text_in_body="Movie recommendation system"
        ),
        Check(
            name="API Check",
            method="GET",
            path=f"{API_PREFIX}/recommendations",
            expected_status=200,
            expected_json_is_list=True
        ),
        Check(
            name="404 Check",
            method="GET",
            path="/non/existent/path",
            expected_status=404
        ),
    ]


    total = len(checks)
    failures: List[str] = []

    print(f"\nRunning {total} checks against {BASE_URL}...")


    for chk in checks:
        error_message = run_check(sess, chk)
        
        if error_message:
            icon = "✗"
            failures.append(f"{chk.name}: {error_message}")
        else:
            icon = "✓"

        
        print(f"[{icon}] {chk.name:<20} ({chk.method} {chk.path})")


    print(f"\nSummary: {total - len(failures)}/{total} passed.")
    
    if failures:
        print("\nFailures:")
        for f in failures:
            print(f"::error:: - {f}")

        return 1


    print("::notice::All tests passed successfully!")
    return 0


if __name__ == "__main__":
    sys.exit(main())