from django import forms
from django.contrib.admin import widgets as admin_widgets
from django.forms.widgets import flatatt
from django.utils.html import conditional_escape
from django.template.loader import render_to_string

from pagedown import settings as pagedown_settings
from pagedown.utils import compatible_staticpath


try:
    from django.utils.encoding import force_unicode
except ImportError: #python3
    # https://docs.djangoproject.com/en/1.5/topics/python3/#string-handling
    from django.utils.encoding import force_text as force_unicode
from django.utils.safestring import mark_safe


class PagedownWidget(forms.Textarea):

    def __init__(self, *args, **kwargs):
        self.show_preview = kwargs.pop('show_preview', pagedown_settings.SHOW_PREVIEW)
        self.template = kwargs.pop('template', pagedown_settings.WIDGET_TEMPLATE)
        self.css = kwargs.pop('css', pagedown_settings.WIDGET_CSS)
        super(PagedownWidget, self).__init__(*args, **kwargs)

    def _media(self):
        return forms.Media(
            css={
                'all': self.css + ('//ajax.googleapis.com/ajax/libs/jqueryui/1.11.1/themes/smoothness/jquery-ui.min.css',)
            },
            js=(
                compatible_staticpath('pagedown/js/Markdown.Converter.js'),
                compatible_staticpath('pagedown/js/Markdown.Sanitizer.js'),
                compatible_staticpath('pagedown/js/Markdown.Editor.js'),
                compatible_staticpath('pagedown/js/djquery_init.js'), #Sets jquery namespace back to $
                '//ajax.googleapis.com/ajax/libs/jqueryui/1.11.1/jquery-ui.min.js',
                compatible_staticpath('pagedown/js/jquery.ajaxfileupload.js'),
                compatible_staticpath('pagedown/js/pagedown_init.js'),
            ))
    media = property(_media)

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        if 'class' not in attrs:
            attrs['class'] = ""
        attrs['class'] += " wmd-input"
        final_attrs = self.build_attrs(attrs, name=name)
        return render_to_string(self.template, {
            'attrs': flatatt(final_attrs),
            'body': conditional_escape(force_unicode(value)),
            'id': final_attrs['id'],
            'show_preview': self.show_preview,
        })



class AdminPagedownWidget(PagedownWidget, admin_widgets.AdminTextareaWidget):
    class Media:
        css = {
            'all': (compatible_staticpath('pagedown/css/pagedown.css'),)
        }
        js = (
            compatible_staticpath('pagedown/js/pagedown.js'),
        )
