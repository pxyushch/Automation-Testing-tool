
class FlakyTestTracker:
    def __init__(self):
        self.flaky_tests = set()

    def record_retry(self, test_name):
        self.flaky_tests.add(test_name)
