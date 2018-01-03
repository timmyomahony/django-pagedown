from django import VERSION, forms
from django.contrib.admin import widgets as admin_widgets
from django.utils.html import conditional_escape
from django.template import Context, loader

# Django 1.7 compatibility
try:
    from django.forms.utils import flatatt
except ImportError:
    from django.forms.util import flatatt

from pagedown import settings as pagedown_settings
from pagedown.utils import compatible_staticpath


# Python 3 compatibility
# https://docs.djangoproject.com/en/1.5/topics/python3/#string-handling
try:
    from django.utils.encoding import force_unicode
except ImportError:
    from django.utils.encoding import force_text as force_unicode


class PagedownWidget(forms.Textarea):

    def __init__(self, *args, **kwargs):
        self.show_preview = kwargs.pop(
            "show_preview", pagedown_settings.SHOW_PREVIEW)
        self.template = kwargs.pop(
            "template", pagedown_settings.WIDGET_TEMPLATE)
        self.css = kwargs.pop("css", pagedown_settings.WIDGET_CSS)
        super(PagedownWidget, self).__init__(*args, **kwargs)

    def _media(self):
        return forms.Media(
            css={
                "all": self.css
            },
            js=(
                compatible_staticpath("pagedown/Markdown.Converter.js"),
                compatible_staticpath(
                    "pagedown-extra/pagedown/Markdown.Converter.js"),
                compatible_staticpath("pagedown/Markdown.Sanitizer.js"),
                compatible_staticpath("pagedown/Markdown.Editor.js"),
                compatible_staticpath("pagedown-extra/Markdown.Extra.js"),
                compatible_staticpath("pagedown_init.js"),
            ))
    media = property(_media)

    def render(self, name, value, attrs=None):
        if value is None:
            value = ""
        if VERSION < (1, 11):
            final_attrs = self.build_attrs(attrs, name=name)
        else:
            final_attrs = self.build_attrs(attrs, {'name': name})

        if "class" not in final_attrs:
            final_attrs["class"] = ""
        final_attrs["class"] += " wmd-input"
        template = loader.get_template(self.template)

        # Compatibility fix:
        # see https://github.com/timmyomahony/django-pagedown/issues/42
        context = {
            "attrs": flatatt(final_attrs),
            "body": conditional_escape(force_unicode(value)),
            "id": final_attrs["id"],
            "show_preview": self.show_preview,
        }
        context = Context(context) if VERSION < (1, 9) else context
        return template.render(context)


class AdminPagedownWidget(PagedownWidget, admin_widgets.AdminTextareaWidget):
    def _media(self):
        return super(AdminPagedownWidget, self).media + forms.Media(
            css={
                "all": (compatible_staticpath("admin/css/pagedown.css"),)
            },
            js=(
                compatible_staticpath("admin/js/pagedown.js"),
            ))
    media = property(_media)
