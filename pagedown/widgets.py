from django import forms
from django.contrib.admin import widgets as admin_widgets
from django.forms.widgets import flatatt
from django.utils.html import conditional_escape
from django.template import Context, loader

from pagedown import settings as pagedown_settings
from pagedown.utils import compatible_staticpath


try:
    from django.utils.encoding import force_unicode
except ImportError:  # python3
    # https://docs.djangoproject.com/en/1.5/topics/python3/#string-handling
    from django.utils.encoding import force_text as force_unicode


class PagedownWidget(forms.Textarea):

    def __init__(self, *args, **kwargs):
        self.show_preview = kwargs.pop("show_preview", pagedown_settings.SHOW_PREVIEW)
        self.template = kwargs.pop("template", pagedown_settings.WIDGET_TEMPLATE)
        self.css = kwargs.pop("css", pagedown_settings.WIDGET_CSS)
        super(PagedownWidget, self).__init__(*args, **kwargs)

    def _media(self):
        return forms.Media(
            css={
                "all": self.css
            },
            js=(
                compatible_staticpath("pagedown/Markdown.Converter.js"),
                compatible_staticpath('pagedown-extra/pagedown/Markdown.Converter.js'),
                compatible_staticpath("pagedown/Markdown.Sanitizer.js"),
                compatible_staticpath("pagedown/Markdown.Editor.js"),
                compatible_staticpath('pagedown-extra/Markdown.Extra.js'),
                compatible_staticpath("pagedown_init.js"),
            ))
    media = property(_media)

    def render(self, name, value, attrs=None):
        if value is None:
            value = ""
        final_attrs = self.build_attrs(attrs, name=name)
        if "class" not in final_attrs:
            final_attrs["class"] = ""
        final_attrs["class"] += " wmd-input"
        template = loader.get_template(self.template)
        context = Context({
            "attrs": flatatt(final_attrs),
            "body": conditional_escape(force_unicode(value)),
            "id": final_attrs["id"],
            "show_preview": self.show_preview,
        })
        return template.render(context)


class AdminPagedownWidget(PagedownWidget, admin_widgets.AdminTextareaWidget):
    class Media:
        css = {
            "all": (compatible_staticpath("admin/css/pagedown.css"),)
        }
        js = (
            compatible_staticpath("admin/js/pagedown.js"),
        )
