from django.urls import path

from pagedown.views import image_upload_view


urlpatterns = [
    path(
        'pagedown/image-upload/',
        image_upload_view,
        name="pagedown-image-upload"),
]
