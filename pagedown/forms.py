from django import forms
from django.conf import settings
from django.core.validators import FileExtensionValidator

from pagedown.widgets import AdminPagedownWidget, PagedownWidget

IMAGE_UPLOAD_EXTENSIONS = getattr(
    settings,
    'PAGEDOWN_IMAGE_UPLOAD_EXTENSIONS', [
        'jpg',
        'jpeg',
        'png',
        'webp'
    ])


class PagedownField(forms.CharField):
    widget = PagedownWidget


class AdminPagedownField(forms.CharField):
    widget = AdminPagedownWidget


class ImageUploadForm(forms.Form):
    image = forms.ImageField(
        required=True,
        validators=[FileExtensionValidator(
            allowed_extensions=IMAGE_UPLOAD_EXTENSIONS)])
