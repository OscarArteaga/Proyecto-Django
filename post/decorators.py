from functools import wraps
from django.contrib.auth.decorators import user_passes_test
from django.conf import settings

def admin_required(function=None):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_staff,
        login_url=settings.LOGIN_URL
    )
    if function:
        return actual_decorator(function)
    return actual_decorator