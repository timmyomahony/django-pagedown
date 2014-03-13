from django import forms
from django.conf import settings
from django.contrib.admin import widgets as admin_widgets
from django.forms.widgets import flatatt
from django.utils.html import conditional_escape
from django.template.loader import render_to_string

from pagedown import settings as pagedown_settings

try:
    from django.utils.encoding import force_unicode
except ImportError: #python3
    # https://docs.djangoproject.com/en/1.5/topics/python3/#string-handling
    from django.utils.encoding import force_text as force_unicode
from django.utils.safestring import mark_safe


def compatible_staticpath(path):
    '''
    Try to return a path compatible all the way back to Django 1.2. If anyone
    has a cleaner or better way to do this let me know!
    '''
    try:
        from django.contrib.staticfiles.storage import staticfiles_storage
        return staticfiles_storage.url(path)
    except ImportError:
        pass
    try:
        return '%s/%s' % (settings.STATIC_URL.rstrip('/'), path)
    except AttributeError:
        pass
    try:
        return '%s/%s' % (settings.PAGEDOWN_URL.rstrip('/'), path)
    except AttributeError:
        pass
    return '%s/%s' % (settings.MEDIA_URL.rstrip('/'), path)


class PagedownWidget(forms.Textarea):
    class Media:
        css = {
            'all': (compatible_staticpath('pagedown/demo/browser/demo.css'),)
        }
        js = (compatible_staticpath('pagedown/Markdown.Converter.js'),
              compatible_staticpath('pagedown/Markdown.Sanitizer.js'),
              compatible_staticpath('pagedown/Markdown.Editor.js'),
              compatible_staticpath('pagedown_init.js'),)

    def __init__(self, *args, **kwargs):
        self.show_preview = kwargs.pop('show_preview', pagedown_settings.SHOW_PREVIEW)
        super(PagedownWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        if 'class' not in attrs:
            attrs['class'] = ""
        attrs['class'] += " wmd-input"
        final_attrs = self.build_attrs(attrs, name=name)
        rendered_html = render_to_string('pagedown/widget.html', {
            'attrs': flatatt(final_attrs),
            'body': conditional_escape(force_unicode(value)),
            'id': final_attrs['id'],
            'show_preview': self.show_preview,
        })
        return mark_safe(rendered_html)


class AdminPagedownWidget(PagedownWidget, admin_widgets.AdminTextareaWidget):
    class Media:
        css = {
            'all': (compatible_staticpath('admin/css/pagedown.css'),)
        }
