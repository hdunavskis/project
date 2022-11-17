import traceback
from django.http import HttpResponse

class ErrorTracebackMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        print(traceback.format_exc())
        return HttpResponse(exception)
