Django Pagedown
===============

Add [Stack Overflow&#39;s &quot;Pagedown&quot; Markdown editor](https://github.com/StackExchange/pagedown/) to your Django Admin or custom form.

![Screenshot of Django Admin with Pagedown initialised](https://github.com/timmyomahony/django-pagedown/blob/master/screenshot.png?raw=true "A screenshot of Pagedown in Django's admin")

## Requirements

Version >= 2.0.0 of `django-pagedown` requires Django 2.1.0 or above (previous versions should support Django all the way back to around 1.1).

## Installation

1. Get the code: `pip install django-pagedown`
2. Add `pagedown.apps.PagedownConfig` to your `INSTALLED_APPS`
3. Collect the static files: `python manage.py collectstatic`

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

```py
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

## Rendering Markdown

`contrib.markdown` was [deprecated in Django 1.5](https://code.djangoproject.com/ticket/18054) meaning you can no longer use the `markdown` filter in your template by default. 

[@wkcd has a good example](https://github.com/timmyomahony/django-pagedown/issues/18#issuecomment-37535535) of how to overcome by installing `django-markdown-deux`: 

```
{% extends 'base.html' %}
{% load markdown_deux_tags %}
	
...
<p>{{ entry.body|markdown }}</p>
...
```

## Image Uploads

You can enable image uploads, allowing your users to upload new images to the server and have them automatically inserted into the Pagedown widget (instead of just adding image URLs):

![Screenshot of Django Admin with image upload enabled](https://github.com/timmyomahony/django-pagedown/blob/master/image-upload.png?raw=true "Screenshot of Django Admin with image upload enabled")

To do so:

1. Make sure you have set a `MEDIA_URL` and `MEDIA_ROOT` so that uploads will be propertly saved
2. Add `PAGEDOWN_IMAGE_UPLOAD_ENABLED=True` to your settings
3. Include the pagedown paths in your `urls.py` so that the upload endpoint is available

```py
    # ...
    urlpatterns = [
        path('', include('pagedown.urls')),
        # ...
    ]
```

This will add the URL `/pagedown/image-upload/` endpoint to your project. You can [see the default view that handles the upload here](https://github.com/timmyomahony/django-pagedown/blob/master/pagedown/views.py)

The following options are available via your settings to tweak how the image upload works:

- `PAGEDOWN_IMAGE_UPLOAD_EXTENSIONS` can be used to limit the extensions allowed for upload (default is `jpg`, `jpeg`, `png`, `svg`, `webp`)
- `PAGEDOWN_IMAGE_UPLOAD_MAX_SIZE` can be used to limit the max size of uploads (default is 10mb)
- `PAGEDOWN_IMAGE_UPLOAD_PATH` can be used to change the path within your media root (default is `pagedown-uploads`)

Check out the `pagedown_init.js` script to [see how the upload is being performed on the client side](https://github.com/timmyomahony/django-pagedown/blob/master/pagedown/static/pagedown_init.js).

### Caveats

Be aware the the default endpoint isn't CSRF protected and also isn't restricted to logged-in users.

## Example

You can see a fully-fledged example of the widget in [`django-pagedown-example`](https://github.com/timmyomahony/django-pagedown-example)
