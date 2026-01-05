# Custom middleware to set Content Security Policy (CSP) header

class CustomCSPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response["Content-Security-Policy"] = (
            "default-src 'self'; object-src 'none'; script-src 'self';"
        )
        return response
