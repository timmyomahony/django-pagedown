from django.conf import settings
from django import forms
from django.contrib.admin import widgets


class PagedownWidget(forms.Textarea):
    template_name = 'pagedown/forms/widgets/default.html'

    def __init__(self, attrs=None, upload_dir=None):
        super(PagedownWidget, self).__init__(attrs=attrs)
        # Add wmd-input class for easier styling
        self.attrs['class'] = '{} wmd-input'.format(
            self.attrs.get('class', ''))
        self.upload_dir = upload_dir

    def get_context(self, name, value, attrs):
        context = super(PagedownWidget, self).get_context(name, value, attrs)
        context["image_upload_enabled"] = getattr(
            settings, 'PAGEDOWN_IMAGE_UPLOAD_ENABLED', False)
        context["upload_dir"] = self.upload_dir
        return context

    class Media:
        css = {
            'all': ('pagedown/demo/browser/demo.css',
                    'pagedown.css')
        }
        js = ('pagedown/Markdown.Converter.js',
              'pagedown-extra/pagedown/Markdown.Converter.js',
              'pagedown/Markdown.Sanitizer.js',
              'pagedown/Markdown.Editor.js',
              'pagedown-extra/Markdown.Extra.js',
              'pagedown_init.js')


class AdminPagedownWidget(PagedownWidget, widgets.AdminTextareaWidget):

    class Media:
        css = {
            'all': ('pagedown/demo/browser/demo.css',
                    'admin/css/pagedown.css',)
        }
        js = ('admin/js/jquery.init.js',
              'admin/js/pagedown.js')
