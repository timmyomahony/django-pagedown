Django Pagedown
===============
[![Gitter](https://badges.gitter.im/Join Chat.svg)](https://gitter.im/timmyomahony/django-pagedown?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

A django app that allows the easy addition of [Stack Overflow&#39;s &quot;Pagedown&quot; Markdown editor](http://code.google.com/p/pagedown/) to a django form field, whether in a custom app or the Django Admin

![Screenshot of Django Admin with Pagedown initialised](https://github.com/timmyomahony/django-pagedown/blob/master/django-pagedown-screenshot.png?raw=true "A screenshot of Pagedown in Django's admin")

## Installation

1. Get the code: `pip install django-pagedown`
2. Add `pagedown` to your `INSTALLED_APPS`
3. Make sure to collect the static files: `python manage.py collectstatic --noinput` (and if you are working in a development environment, make sure [you are properly serving your static files](https://docs.djangoproject.com/en/1.9/howto/static-files/#serving-static-files-during-development))

Note that this package will install a cloned copy (git submodule) of the Pagedown library from [http://github.com/timmyomahony/pagedown/](http://github.com/timmyomahony/pagedown/).

#### Alternative Installation

If you don't like PyPi (or are having problems with it) you can manually install the pacakge:

 - via pip from GitHub: `pip install -e git+https://timmyomahony@github.com/timmyomahony/django-pagedown.git#egg=django-pagedown`
 - manually clone from Github:
     - `git clone https://timmyomahony@github.com/timmyomahony/django-pagedown.git`
     - `cd django-pagedown`
     - `git submodule update --init`

## Markdown Safety

Remember that this library doesn't render your markdown for you outside of the admin widget nor does it do any internal sanitization. Markdown can accept any valid HTML so you have to be careful and make sure you are rendering the output of any untrusted input safely (with [`django-markdown-deux`](https://github.com/trentm/django-markdown-deux) for example), otherwise you could have users embedding scripts in your pagedown text areas

## Usage

The widget can be used both inside the django admin or independendly. 

#### Inside the Django Admin:

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

#### Outside the Django Admin:

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

## Showing/Hiding the Preview Box

You can control whether or not to show the dynamically rendered preview box below the pagedown widget in two ways: 

 - **Globally:** by using the `PAGEDOWN_SHOW_PREVIEW` option in your `settings.py` (this is mentioned further down the page). This will enable/disable the preview for *all* pagedown widgets throughout your application. 

 - **Per Widget:** by supplying a `show_preview` keyword argument when initialising your widget instance in your form. This gives you finer control over which of the fields can make use of the preview when rendering the pagedown widget. Note that this approach will take preference over the `PAGEDOWN_SHOW_PREVIEW` option. 

    ```python
    # ...

    class AlbumForm(forms.ModelForm):
        # ...
        description = forms.CharField(widget=PagedownWidget(show_preview=False))
    
        class Meta:
            model = Album
            fields = ['description', ]
    ```		

## Customizing the Widget Template/HTML

If you want to customize the HTML used to render the pagedown widget altogether, you can. There are two ways: 

- **Globally:** by default, the template used to render the pagedown widget is located at `pagedown/widgets/default.html`.  
  - You can override this template by creating `pagedown/widgets/default.html` within your own template directory. This will take preference if you are using Django's default template loading system
  - You can use the `PAGEDOWN_WIDGET_TEMPLATE` settings to point to a different template file
- **Per Widget:** by supplying a `template` keyword argument when initialising your widget instance in your form. This should be the path to the template you wish to use to render this instance. 

    ```python  
    # ...

    class AlbumForm(forms.ModelForm):
        # ...
        description = forms.CharField(widget=PagedownWidget(template="path/to/template.html"))
        
        class Meta:
            model = Album
            fields = ['description', ]
    ```

## Customizing the CSS

If you want to change the CSS used to display the widgets, you also can. Again, there are two ways: 

 - **Globally:** You can specify the CSS files to be included by the widget by providing a tuple of paths via a `PAGEDOWN_WIDGET_CSS` variable in your `settings.py`

		# Import the default pagedown css first, then our custom CSS sheet
		# to avoid having to specify all the default styles
		PAGEDOWN_WIDGET_CSS = ('pagedown/demo/browser/demo.css', "pagedown/custom.css",)
 
- **Per Widget:** by supplying a `css` keyword argument when initialising your widget instance in your form

    ```python
    # ...
    	
    class AlbumForm(forms.ModelForm):
        # ...
	    description = forms.CharField(widget=PagedownWidget(css=("custom/css1.css", "custom/css2.css")))
    
        class Meta:
            model = Album
            fields = ['description', ]
    ```

## Options

The following options can be added to your default `settings.py` file to control certain aspects of `django-pagedown`. Note that changing these will affect **all** instances of the pagedown widget throughout your app.:

- `PAGEDOWN_SHOW_PREVIEW` (boolean): whether or not to show the dynamic markdown preview below the markdown text area for the pagedown widgets. The default is `True`.
- `PAGEDOWN_WIDGET_TEMPLATE` (string): the template used to render the pagedown widget. The default template is located in `pagedown/widgets/default.html`. 
- `PAGEDOWN_WIDGET_CSS` (tuple): the path to the CSS file to be used by the pagedown widget. The default path is `pagedown/

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

## TODO

- Add support for images uploading or hooks into the likes of `django-filer` etc. 
