Django Pagedown
===============

A django app that allows the easy addition of [Stack Overflow&#39;s &quot;Pagedown&quot; Markdown editor](http://code.google.com/p/pagedown/) to a django form field, whether in a custom app or the Django Admin

---

![Screenshot of Django Admin with Pagedown initialised](https://github.com/timmyomahony/django-pagedown/blob/master/django-pagedown-screenshot.png?raw=true "A screenshot of Pagedown in Django's admin")

---

## Installation ##

1. Get the code: `pip install django-pagedown`
2. Add `pagedown` to your `INSTALLED_APPS`
3. Make sure to collect the static files: `python manage.py collectstatic --noinput`

Note that this package will install a cloned copy (git submodule)of the Pagedown library from [http://github.com/timmyomahony/pagedown/](http://github.com/timmyomahony/pagedown/).

If you don't like (or are having problems with) PyPi, you can alternatively install:

 - Via pip from GitHub: `pip install -e git+https://timmyomahony@github.com/timmyomahony/django-pagedown.git#egg=django-pagedown`
 - Manually clone from Github:
     - `git clone https://timmyomahony@github.com/timmyomahony/django-pagedown.git`
     - `cd django-pagedown`
     - `git submodule update --init`

---

## Usage ##

**Inside the Django Admin:**

If you want to use the pagedown editor in a django admin field, there are numerous possible approaches:

To use it in **all** `TextField`'s in you admin form:

    from pagedown.widgets import AdminPagedownWidget
    from django.db import models


    class FooModelAdmin(models.ModelAdmin):
    	formfield_overrides = {
        	models.TextField: {'widget': AdminPagedownWidget },
    	}

Alternatively, to only use it on **particular fields**, first create a form (in `forms.py`):

    from pagedown.widgets import AdminPagedownWidget
    from django import forms
    from models import FooModel


    class FooModelForm(forms.ModelForm):
        a_text_field = forms.CharField(widget=AdminPagedownWidget())
        another_text_field = forms.CharField(widget=AdminPagedownWidget())

        class Meta:
	    model = FooModel

and in your `admin.py`:

    from forms import FooModelForm
    from models import FooModel
    from django.contrib import admin


    class FooModelAdmin(admin.ModelAdmin):
    	form = FooModelForm

    admin.site.register(FooModel, FooModelAdmin)

**Outside the Django Admin:**

To use the widget outside of the django admin, first create a form similar to the above but using the basic `PagedownWidget`:

    from pagedown.widgets import PagedownWidget
    from django import forms
    from models import FooModel


    class FooModelForm(forms.ModelForm):
        a_text_field = forms.CharField(widget=PagedownWidget())
        another_text_field = forms.CharField(widget=PagedownWidget())

        class Meta:
	    model = FooModel


Then define your urls/views:

    from forms import FooModelForm
    from django.views.generic import FormView
    from django.conf.urls import patterns, url

    urlpatterns = patterns('',
        url(r'^$', FormView.as_view(
            template_name="baz.html",
            form_class=FooModelForm)),
    )

then create the template and load the javascipt and css required to create the editor:

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
    
---

## Showing/Hiding the Preview Box ##

You can control whether or not to show the dynamically rendered preview box below the pagedown widget in two ways: 

 - **Globally:** by using the `PAGEDOWN_SHOW_PREVIEW` option in your `settings.py` (this is mentioned further down the page). This will enable/disable the preview for *all* pagedown widgets throughout your application. 
 

 - **Per Widget:** by supplying a `show_preview` keyword argument when initialising your widget instance in your form. This gives you finer control over which of the fields can make use of the preview when rendering the pagedown widget. Note that this approach will take preference over the `PAGEDOWN_SHOW_PREVIEW` option. 
  
		...

		class FooModelForm(forms.ModelForm):
			foo = forms.CharField(widget=PagedownWidget(show_preview=False))
        
        	class Meta:
    			model = FooModel
    			
---

## Customizing the Widget Template/HTML ##

If you want to customize the HTML used to render the pagedown widget altogether, you can. There are two ways: 

- **Globally:** by default, the template used to render the pagedown widget is located at `pagedown/widgets/default.html`.  
  - You can override this template by creating `pagedown/widgets/default.html` within your own template directory. This will take preference if you are using Django's default template loading system
  - You can use the `PAGEDOWN_DEFAULT_TEMPLATE` settings to point to a different template file
- **Per Widget:** by supplying a `template` keyword argument when initialising your widget instance in your form. This should be the path to the template you wish to use to render this instance. 
  
    	...
    	
    	class FooModelForm(forms.ModelForm):
			foo = forms.CharField(widget=PagedownWidge(template="path/to/template.html"))
        
        	class Meta:
    			model = FooModel
---

## Customizing the CSS ##

If you want to change the CSS used to display the widgets, you also can. Again, there are two ways: 

 - **Globally:** You can specify the CSS files to be included by the widget by providing a tuple of paths via a `PAGEDOWN_WIDGET_CSS` variable in your `settings.py`

		# Import the default pagedown css first, then our custom CSS sheet
		# to avoid having to specify all the default styles
		PAGEDOWN_WIDGET_CSS = ('pagedown/demo/browser/demo.css', "pagedown/custom.css",)
 
- **Per Widget:** by supplying a `css` keyword argument when initialising your widget instance in your form

  
    	...
    	
    	class FooModelForm(forms.ModelForm):
			foo = forms.CharField(widget=PagedownWidge(css=("custom/css1.css", "custom/css2.css")))
        
        	class Meta:
    			model = FooModel


---

## Options ##

The following options can be added to your default `settings.py` file to control certain aspects of `django-pagedown`. Note that changing these will affect **all** instances of the pagedown widget throughout your app.:

- `PAGEDOWN_SHOW_PREVIEW` (boolean): whether or not to show the dynamic markdown preview below the markdown text area for the pagedown widgets. The default is `True`.
- `PAGEDOWN_DEFAULT_TEMPLATE` (string): the template used to render the pagedown widget. The default template is located in `pagedown/widgets/default.html`. 
- `PAGEDOWN_WIDGET_CSS` (tuple): the path to the CSS file to be used by the pagedown widget. The default path is `pagedown/

---

## Rendering Markdown In Your Template ##

`contrib.markdown` was [depreciated in Django 1.5](https://code.djangoproject.com/ticket/18054) meaning you can no longer use the `markdown` filter in your template by default. 

[@wkcd has a good example](https://github.com/timmyomahony/django-pagedown/issues/18#issuecomment-37535535) of how to overcome by installing `django-markdown-deux`: 

	{% extends 'base.html' %}
	{% load markdown_deux_tags %}
	
	...
	<p>{{ entry.body|markdown }}</p>
	...
	
--- 

## TODO ##

- Add support for images uploading or hooks into the likes of `django-filer` etc. 
