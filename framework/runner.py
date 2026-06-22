
from concurrent.futures import ThreadPoolExecutor

class ParallelTestRunner:
    def __init__(self, max_workers=4):
        self.max_workers = max_workers

    def run_suite(self, test_cases):
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            return list(executor.map(lambda tc: tc(), test_cases))
