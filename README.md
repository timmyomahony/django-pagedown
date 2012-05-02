Django Pagedown
===============

A django app that allows the easy addition of [Stack Overflow&#39;s &quot;Pagedown&quot; Markdown editor](http://code.google.com/p/pagedown/) to a django form field, whether in a custom app or the Django Admin

---

![Screenshot of Django Admin with Pagedown initialised](https://github.com/timmyomahony/django-pagedown/blob/master/django-pagedown-screenshot.png?raw=true "A screenshot of Pagedown in Django's admin")

---

#### Installation ####

- Install via pip: `pip install -e https://timmyomahony@github.com/timmyomahony/django-pagedown.git#egg=django-pagedown` 
- Add `pagedown` to your `INSTALLED_APPS`

#### Usage ####

If you want to use the pagedown editor in a django admin field, there are numerous possible approaches:

To use it in **all** `TextField`'s in you admin form:

	from pagedown.widgets import AdminPageDownWidget
    class FooModelAdmin(models.ModelAdmin):
    	formfield_overrides = {
        	models.TextField: {'widget': AdminPageDownWidget },
    	}
    	
Alternatively, to only use it on particular fields, first create a form (in `forms.py`): 

	from pagedown.widgets import AdminPageDownWidget
	class FooModelForm(forms.ModelForm):
		a_text_field = forms.TextField(widget=AdminPageDownWidget())		
		another_text_field = forms.TextField(widget=AdminPageDownWidget())	
		
		class Meta:
			model = FooModel
			
and in your `admin.py`:

	from forms import FooModelForm
    class FooModelAdmin(models.ModelAdmin):
    	form = FooModelForm   
 
 
#### Notes ####
   	
* There are two widgets, `AdminPageDownWidget` and `PageDownWidget`. The only difference is that `AdminPageDownWidget` includes extra CSS to make the preview area and input pretty in the django admin. If you are using the editor for your own app, you will need to supply CSS to do this. 