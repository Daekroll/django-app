from django.http import HttpRequest
import time


def set_useragent_on_request_middleware(get_response):
    def middleware(request: HttpRequest):
        request.user_agent = request.META.get("HTTP_USER_AGENT", "unknown")
        return get_response(request)

    return middleware


import time
from django.http import JsonResponse


class TimeCountRequest:
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_timestamps = {}

    def __call__(self, request):
        user_ip = request.META.get('REMOTE_ADDR')
        current_time = time.time()

        if user_ip in self.request_timestamps:
            last_request_time = self.request_timestamps[user_ip]
            time_slice = current_time - last_request_time
            print(time_slice)

            if time_slice < 0:
                return JsonResponse({"error": "Слишком много запросов, попробуйте позже."}, status=429)

        self.request_timestamps[user_ip] = current_time

        response = self.get_response(request)
        return response
