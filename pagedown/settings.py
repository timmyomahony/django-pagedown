from django.conf import settings


SHOW_PREVIEW = getattr(settings, 'PAGEDOWN_SHOW_PREVIEW', True)
WIDGET_TEMPLATE = getattr(settings, 'PAGEDOWN_WIDGET_TEMPLATE', 'pagedown/widgets/default.html')
WIDGET_CSS = getattr(settings, 'PAGEDOWN_WIDGET_CSS', ('pagedown/css/demo.css', ))

PAGEDOWN_RESTRICT_BY_USER = getattr(settings, 'PAGEDOWN_RESTRICT_BY_USER', False)

settings.PAGEDOWN_UPLOAD_PATH = getattr(settings, 'PAGEDOWN_UPLOAD_PATH', 'uploads/')
