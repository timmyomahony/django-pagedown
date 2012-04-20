from django import forms
from widgets import AdminPagedownWidget

class PagedownForm(forms.Form):
    """ An example form that includes the javascript required
    for PageDown automatically """
    
    body = forms.CharField(widget=AdminPagedownWidget())