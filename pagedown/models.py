from django.db import models

class PagedownField(models.TextField):
    pass

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^pagedown\.models\.PagedownField"])
except ImportError:
    pass
