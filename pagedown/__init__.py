import django

VERSION = ('2', '2', '0')

if django.VERSION < (3, 2):
    default_app_config = 'pagedown.apps.PagedownConfig'
