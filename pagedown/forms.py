from django import forms
from .widgets import AdminPagedownWidget, PagedownWidget, BootstrapPagedownWidget


class PagedownField(forms.CharField):
    ''' A simple CharField that allows us avoid having to write widget code '''
    widget = PagedownWidget


class AdminPagedownField(forms.CharField):
    ''' A simple CharField that allows us avoid having to write widget code '''
    widget = AdminPagedownWidget

class BootstrapPagedownField(forms.CharField):
    ''' A simple CharField that allows us avoid having to write widget code '''
    widget = BootstrapPagedownWidget

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^pagedown\.forms\.PagedownField"])
    add_introspection_rules([], ["^pagedown\.forms\.AdminPagedownField"])
    add_introspection_rules([], ["^pagedown\.forms\.BootstrapPagedownField"])
except ImportError:
    raise
