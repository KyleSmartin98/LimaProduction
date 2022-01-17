import pytz
from django.utils import timezone
class TimezoneMiddleware(object):
    """
    Middleware to properly handle the users timezone
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            timezone.activate(pytz.timezone(request.user.profile.timezone))
        else:
            timezone.deactivate()

        response = self.get_response(request)
        return response