from django.conf import settings


SHOW_PREVIEW = getattr(settings, 'PAGEDOWN_SHOW_PREVIEW', True)
