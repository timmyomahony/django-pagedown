from django.conf import settings

SHOW_PREVIEW = getattr(settings, "PAGEDOWN_SHOW_PREVIEW", True)
WIDGET_TEMPLATE = getattr(
    settings, "PAGEDOWN_WIDGET_TEMPLATE", "pagedown/widgets/default.html")
WIDGET_CSS = getattr(
    settings, "PAGEDOWN_WIDGET_CSS", ("pagedown/demo/browser/demo.css",))
EXTENSIONS = getattr(settings, "PAGEDOWN_EXTENSIONS", [])
