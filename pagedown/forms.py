from django import forms

from .widgets import AdminPagedownWidget, PagedownWidget


class PagedownField(forms.CharField):

    ''' A simple CharField that allows us avoid having to write widget code '''

    widget = PagedownWidget


class AdminPagedownField(forms.CharField):

    ''' A simple CharField that allows us avoid having to write widget code '''

    widget = AdminPagedownWidget


try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^pagedown\.forms\.PagedownField"])
    add_introspection_rules([], ["^pagedown\.forms\.AdminPagedownField"])
except ImportError:
    raise
