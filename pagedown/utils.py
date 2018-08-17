from django import VERSION
from django.conf import settings


def compatible_staticpath(path):
    """
    Try to return a path to static the static files compatible all
    the way back to Django 1.2. If anyone has a cleaner or better
    way to do this let me know!
    """

    if VERSION >= (1, 10):
        # Since Django 1.10, forms.Media automatically invoke static
        # lazily on the path if it is relative.
        return path
    try:
        # >= 1.4
        from django.templatetags.static import static
        return static(path)
    except ImportError:
        pass
    try:
        # >= 1.3
        return '%s/%s' % (settings.STATIC_URL.rstrip('/'), path)
    except AttributeError:
        pass
    try:
        return '%s/%s' % (settings.PAGEDOWN_URL.rstrip('/'), path)
    except AttributeError:
        pass
    return '%s/%s' % (settings.MEDIA_URL.rstrip('/'), path)
