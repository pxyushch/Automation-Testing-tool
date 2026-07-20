
def intercept_api_calls(page, endpoint, mock_response):
    def handle_route(route):
        route.fulfill(status=200, content_type="application/json", body=mock_response)
    page.route(f"**/{endpoint}**", handle_route)
