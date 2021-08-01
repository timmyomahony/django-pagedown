import os
import uuid
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.exceptions import PermissionDenied, ImproperlyConfigured
from django.contrib.auth.decorators import login_required

from pagedown.forms import ImageUploadForm


IMAGE_UPLOAD_PATH = getattr(
    settings, 'PAGEDOWN_IMAGE_UPLOAD_PATH', 'pagedown-uploads')
IMAGE_UPLOAD_UNIQUE = getattr(
    settings, 'PAGEDOWN_IMAGE_UPLOAD_UNIQUE', False)
IMAGE_UPLOAD_ENABLED = getattr(
    settings, 'PAGEDOWN_IMAGE_UPLOAD_ENABLED', False)


def make_unique_path(dir_name, file_name):
    """
    Create a unique path for a file in a certain directory.

    Appends '-%d' to the file name to make it unique - if necessary-
    Args:
        dir_name (str): the directory where the file will be placed (absolute)
        file_name (str): the initial file name to use

    Returns:
        unique file name based on 'file_name'
    """
    unique_fn, ext = os.path.splitext(file_name)
    dir_name = os.path.abspath(dir_name)
    i = 0
    while os.path.exists(os.path.join(dir_name, unique_fn + ext)):
        i += 1
        if i > 1000:
            raise ValueError("Failed to find unique file name for %s in %s" % (file_name, dir_name))
        unique_fn = "%s-%d" % (unique_fn, i)

    return unique_fn + ext


@login_required
@csrf_exempt
def image_upload_view(request):
    if not request.method == 'POST':
        raise PermissionDenied()

    if not IMAGE_UPLOAD_ENABLED:
        raise ImproperlyConfigured('Image upload is disabled')

    form = ImageUploadForm(request.POST, request.FILES)
    if form.is_valid():
        image = request.FILES['image']
        # check optional upload dir override
        upload_dir_override = request.POST.get("upload-dir-override", "")
        if upload_dir_override:
            file_name = make_unique_path(os.path.join(settings.MEDIA_ROOT, upload_dir_override),
                                         image.name)
            path_args = [upload_dir_override, file_name]
        else:
        path_args = [IMAGE_UPLOAD_PATH, image.name]
        if IMAGE_UPLOAD_UNIQUE:
            path_args.insert(1, str(uuid.uuid4()))

        path = os.path.join(*path_args)
        path = default_storage.save(path, image)
        url = default_storage.url(path)
        return JsonResponse({'success': True, 'url': url})

    return JsonResponse({'success': False, 'error': form.errors})
