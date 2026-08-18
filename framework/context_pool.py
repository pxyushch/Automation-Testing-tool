
class BrowserContextPool:
    def __init__(self, browser):
        self.browser = browser
        self.pool = []

    def get_context(self):
        return self.pool.pop() if self.pool else self.browser.new_context()

    def release_context(self, context):
        self.pool.append(context)
