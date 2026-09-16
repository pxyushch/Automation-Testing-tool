
class BasePage:
    def __init__(self, page):
        self.page = page

    def navigate(self, url):
        self.page.goto(url)

    def click_element(self, selector):
        self.page.locator(selector).click()
