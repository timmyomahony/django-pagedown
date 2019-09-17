from django import forms

from pagedown.widgets import AdminPagedownWidget, PagedownWidget


class PagedownField(forms.CharField):
    """A simple CharField that allows us avoid having to write widget code"""
    widget = PagedownWidget


class AdminPagedownField(forms.CharField):
    """A simple CharField that allows us avoid having to write widget code"""
    widget = AdminPagedownWidget
