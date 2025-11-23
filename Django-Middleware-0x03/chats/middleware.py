import datetime
import os
from django.conf import settings
from django.http import HttpResponseForbidden

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user.username if request.user.is_authenticated else 'Anonymous'
        log_message = f"{datetime.datetime.now()} - User: {user} - Path: {request.path}\n"
        log_file_path = os.path.join(settings.BASE_DIR, 'requests.log')
        with open(log_file_path, 'a') as log_file:
            log_file.write(log_message)
        response = self.get_response(request)
        return response

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now = datetime.datetime.now().time()
        start_time = datetime.time(9, 0)  # 9 AM
        end_time = datetime.time(18, 0)  # 6 PM
        if not (start_time <= now <= end_time):
            return HttpResponseForbidden("Access denied outside business hours (9 AM to 6 PM).")
        response = self.get_response(request)
        return response

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests = {}  # {ip: [(timestamp, count)]}

    def __call__(self, request):
        ip = self.get_client_ip(request)
        now = datetime.datetime.now()
        window_start = now - datetime.timedelta(minutes=1)
        if ip not in self.requests:
            self.requests[ip] = []
        # Clean old entries
        self.requests[ip] = [t for t in self.requests[ip] if t > window_start]
        if request.method == 'POST' and 'messages' in request.path:
            if len(self.requests[ip]) >= 5:
                return HttpResponseForbidden("Rate limit exceeded: 5 messages per minute.")
            self.requests[ip].append(now)
        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if not (request.user.is_staff or request.user.is_superuser):
                return HttpResponseForbidden("Access denied: Admin or moderator role required.")
        response = self.get_response(request)
        return response