from django.contrib.auth.models import AnonymousUser
from django.core.mail import mail_admins
from rest_framework.throttling import SimpleRateThrottle, BaseThrottle

from rest_framework.compat import is_authenticated


class UserRateThrottleWithEmail(SimpleRateThrottle):
    def throttle_failure(self):
        """
        Called when a request to the API has failed due to throttling.
        """
        # TODO: Sentry notification
        # if self.request.user is not AnonymousUser:
        #     mail_admins('Alert: User Throttled', 'The following user has been throttled: %s (exceeded %s)' % (self.request.user, self.rate))
        return False


class UserSecondRateThrottle(UserRateThrottleWithEmail):
    """
    Limits the rate of API calls that may be made by a given user.
    The user id will be used as a unique cache key if the user is
    authenticated.  For anonymous requests, the IP address of the request will
    be used.
    """
    scope = 'second_anon'

    def get_cache_key(self, request, view):
        self.request = request
        if is_authenticated(request.user):
            if request.user.info.company.owner.groups.filter(name='badger').exists():
                return None  # do not throttle companies with the badger package.
            else:
                ident = request.user.pk
                self.scope = 'second_free'
                self.rate = self.get_rate()
                self.num_requests, self.duration = self.parse_rate(self.rate)

        else:
            ident = self.get_ident(request)
            self.scope = 'second_anon'
            self.rate = self.get_rate()
            self.num_requests, self.duration = self.parse_rate(self.rate)

        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }


class UserHourRateThrottle(UserRateThrottleWithEmail):
    """
    Limits the rate of API calls that may be made by a given user.
    The user id will be used as a unique cache key if the user is
    authenticated.  For anonymous requests, the IP address of the request will
    be used.
    """
    scope = 'hour_anon'

    def get_cache_key(self, request, view):
        self.request = request
        if is_authenticated(request.user):
            if request.user.info.company.owner.groups.filter(name='badger').exists():
                return None  # do not throttle companies with the badger package.
            else:
                ident = request.user.pk
                self.scope = 'hour_free'
                self.rate = self.get_rate()
                self.num_requests, self.duration = self.parse_rate(self.rate)

        else:
            ident = self.get_ident(request)
            self.scope = 'hour_anon'
            self.rate = self.get_rate()
            self.num_requests, self.duration = self.parse_rate(self.rate)

        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }


class UserDayRateThrottle(UserRateThrottleWithEmail):
    """
    Limits the rate of API calls that may be made by a given user.
    The user id will be used as a unique cache key if the user is
    authenticated.  For anonymous requests, the IP address of the request will
    be used.
    """
    scope = 'day_anon'

    def get_cache_key(self, request, view):
        self.request = request
        if is_authenticated(request.user):
            if request.user.info.company.owner.groups.filter(name='badger').exists():
                return None  # do not throttle companies with the badger package.
            else:
                ident = request.user.pk
                self.scope = 'day_free'
                self.rate = self.get_rate()
                self.num_requests, self.duration = self.parse_rate(self.rate)

        else:
            ident = self.get_ident(request)
            self.scope = 'day_anon'
            self.rate = self.get_rate()
            self.num_requests, self.duration = self.parse_rate(self.rate)

        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }


class NoThrottling(BaseThrottle):
    def allow_request(self, request, view):
        return True