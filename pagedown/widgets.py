from django import forms
from django.conf import settings
from django.contrib.admin import widgets as admin_widgets
from django.forms.widgets import flatatt
from django.utils.html import conditional_escape
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe

STATIC_URL = settings.STATIC_URL.rstrip('/')

class PagedownWidget(forms.Textarea):
    class Media:
        css = {
            'all': ('pagedown/demo/browser/demo.css',)
        }
        js = ('%s/pagedown/Markdown.Converter.js' % STATIC_URL,
              '%s/pagedown/Markdown.Sanitizer.js' % STATIC_URL,
              '%s/pagedown/Markdown.Editor.js' % STATIC_URL,
              '%s/pagedown_init.js' % STATIC_URL,)

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        if 'class' not in attrs:
            attrs['class'] = ""
        attrs['class'] += " wmd-input"
        final_attrs = self.build_attrs(attrs, name=name)
        html = """
            <div class="wmd-wrapper" id="test-wmd">
                <div class="wmd-panel">
                    <div id="%(id)s_wmd_button_bar"></div>
                    <textarea%(attrs)s>%(body)s</textarea>
                </div>
                <div id="%(id)s_wmd_preview" class="wmd-panel wmd-preview"></div>
            </div>
            """ % {
                'attrs': flatatt(final_attrs),
                'body': conditional_escape(force_unicode(value)),
                'id': final_attrs['id'],
            }
        return mark_safe(html)


class AdminPagedownWidget(admin_widgets.AdminTextareaWidget, PagedownWidget):
    class Media:
        css = {
            'all': ('admin/css/pagedown.css',)
        }
