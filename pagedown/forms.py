from django import forms

class PageDownForm(forms.Form):
    """ An example form that includes the javascript required
    for PageDown automatically """
    
    body = forms.TextField(widget=PageDownWidget())
    
    class Media:
        js = ("pagedown/Markdown.Editor.js")