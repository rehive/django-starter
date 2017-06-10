from rest_framework.throttling import BaseThrottle


class NoThrottling(BaseThrottle):
    def allow_request(self, request, view):
        return True