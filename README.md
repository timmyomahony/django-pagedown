Django Pagedown
===============

A django app that allows the easy addition of [Stack Overflow&#39;s &quot;Pagedown&quot; Markdown editor](http://code.google.com/p/pagedown/) to a django form field, whether in a custom app or the Django Admin

---

![Screenshot of Django Admin with Pagedown initialised](https://github.com/timmyomahony/django-pagedown/blob/master/django-pagedown-screenshot.png?raw=true "A screenshot of Pagedown in Django's admin")

---

#### Installation ####

1. Get the code: `pip install django-pagedown`
2. Add `pagedown` to your `INSTALLED_APPS`

Note that this package will install a cloned copy (git submodule)of the Pagedown library from [http://github.com/timmyomahony/pagedown/](http://github.com/timmyomahony/pagedown/).

If you don't like (or are having problems with) PyPi, you can alternatively install: 

 - Via pip from GitHub: `pip install -e https://timmyomahony@github.com/timmyomahony/django-pagedown.git#egg=django-pagedown`
 - Manually clone from Github: 
     - `git clone https://timmyomahony@github.com/timmyomahony/django-pagedown.git`  
     - `cd django-pagedown`
     - `git submodule update --init`


#### Usage ####

If you want to use the pagedown editor in a django admin field, there are numerous possible approaches:

To use it in **all** `TextField`'s in you admin form:

    from pagedown.widgets import AdminPagedownWidget
    from django.db import models
    

    class FooModelAdmin(models.ModelAdmin):
    	formfield_overrides = {
        	models.TextField: {'widget': AdminPagedownWidget },
    	}
    	
Alternatively, to only use it on particular fields, first create a form (in `forms.py`): 

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
 
 
#### Notes ####
   	
* There are two widgets, `AdminPageDownWidget` and `PageDownWidget`. The only difference is that `AdminPageDownWidget` includes extra CSS to make the preview area and input pretty in the django admin. If you are using the editor for your own app, you will need to supply CSS to do this. 
