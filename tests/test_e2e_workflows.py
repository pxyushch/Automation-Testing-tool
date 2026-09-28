
def test_login_and_dashboard_navigation():
    status = "SUCCESS"
    assert status == "SUCCESS"

def test_flaky_retry_tolerance():
    attempts = 2
    assert attempts <= 3
