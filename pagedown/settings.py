from django.conf import settings


SHOW_PREVIEW = getattr(settings, 'PAGEDOWN_SHOW_PREVIEW', True)
WIDGET_TEMPLATE = getattr(settings, 'PAGEDOWN_WIDGET_TEMPLATE', 'pagedown/widgets/default.html')