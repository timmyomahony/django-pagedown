Django Pagedown
===============

A django app that allows the easy addition of [Stack Overflow&#39;s &quot;Pagedown&quot; Markdown editor](https://github.com/StackExchange/pagedown/) to a django form field, whether in a custom app or the Django Admin

![Screenshot of Django Admin with Pagedown initialised](https://github.com/timmyomahony/django-pagedown/blob/master/django-pagedown-screenshot.png?raw=true "A screenshot of Pagedown in Django's admin")

## Requirements

The widget has been vastly simplified so that it's easier to drop-into your projects and easier to customise. Version >= 2.0.0 requires Django 2.1.0 or above.

## Installation

1. Get the code: `pip install django-pagedown`
2. Add `pagedown` to your `INSTALLED_APPS`
3. Make sure to collect the static files: `python manage.py collectstatic --noinput` (and if you are working in a development environment, make sure [you are properly serving your static files](https://docs.djangoproject.com/en/1.9/howto/static-files/#serving-static-files-during-development))

## Markdown Safety

Remember that this library doesn't render your markdown for you outside of the admin widget nor does it do any internal sanitization. Markdown can accept any valid HTML so you have to be careful and make sure you are rendering the output of any untrusted input safely (with [`django-markdown-deux`](https://github.com/trentm/django-markdown-deux) for example), otherwise you could have users embedding scripts in your pagedown text areas

## Usage

The widget can be used both inside the django admin or independendly. 

### Inside the Django Admin:

If you want to use the pagedown editor in a django admin field, there are numerous possible approaches:

- To use it in **all** `TextField`'s in your admin form:

    ```python
    from django.contrib import admin
    from django.db import models

    from pagedown.widgets import AdminPagedownWidget


    class AlbumAdmin(admin.ModelAdmin):
        formfield_overrides = {
            models.TextField: {'widget': AdminPagedownWidget },
        }
    ```
- To only use it on **particular fields**, first create a form (in `forms.py`):

    ```python
    from django import forms
    
    from pagedown.widgets import AdminPagedownWidget
    
    from music.models import Album

    class AlbumForm(forms.ModelForm):
        name = forms.CharField(widget=AdminPagedownWidget())
        description = forms.CharField(widget=AdminPagedownWidget())

        class Meta:
            model = Album
            fields = "__all__"
    ```

    and in your `admin.py`:

    ```python
    from django.contrib import admin
    
    from forms import FooModelForm
    from models import FooModel

    @admin.register(FooModel)
    class FooModelAdmin(admin.ModelAdmin):
        form = FooModelForm
        fields = "__all__"
    ```

### Outside the Django Admin:

To use the widget outside of the django admin, first create a form similar to the above but using the basic `PagedownWidget`:

```python
from django import forms

from pagedown.widgets import PagedownWidget

from music.models import Album


class AlbumForm(forms.ModelForm):
    name = forms.CharField(widget=PagedownWidget())
    description = forms.CharField(widget=PagedownWidget())

    class Meta:
        model = Album
        fields = ["name", "description"]
```

Then define your urls/views:

```
from django.views.generic import FormView
from django.conf.urls import patterns, url

from music.forms import AlbumForm

urlpatterns = patterns('',
    url(r'^$', FormView.as_view(template_name="baz.html",
                                form_class=AlbumForm)),)
```

then create the template and load the javascipt and css required to create the editor:

```html
<html>
    <head>
        {{ form.media }}
    </head>
    <body>
        <form ...>
            {{ form }}
        </form>
    </body>
</html>
```

## Customizing the Widget

If you want to customize the widget, the easiest way is to simply extend it:

```py
from pagedown.widgets import PagedownWidget


class MyNewWidget(PagedownWidget):
    template_name = '/custom/template.html'

    class Media:
        css = {
            'all': ('custom/stylesheets.css,)
        }
        js = ('custom/javascript.js',)
```

## Rendering Markdown In Your Template

`contrib.markdown` was [depreciated in Django 1.5](https://code.djangoproject.com/ticket/18054) meaning you can no longer use the `markdown` filter in your template by default. 

[@wkcd has a good example](https://github.com/timmyomahony/django-pagedown/issues/18#issuecomment-37535535) of how to overcome by installing `django-markdown-deux`: 

```
{% extends 'base.html' %}
{% load markdown_deux_tags %}
	
...
<p>{{ entry.body|markdown }}</p>
...
```
