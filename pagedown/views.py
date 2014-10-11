from datetime import datetime
import os

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
from django.core.files.storage import default_storage



def get_upload_filename(upload_name, user):
    # If PAGEDOWN_RESTRICT_BY_USER is True upload file to user specific path.
    if getattr(settings, 'PAGEDOWN_RESTRICT_BY_USER', False):
        user_path = user.username
    else:
        user_path = ''

    # Generate date based path to put uploaded file.
    date_path = datetime.now().strftime('%Y/%m/%d')

    # Complete upload path (upload_path + date_path).
    upload_path = os.path.join(
        settings.PAGEDOWN_UPLOAD_PATH, user_path, date_path)

    return default_storage.get_available_name(os.path.join(upload_path, upload_name))


@login_required
@csrf_exempt
def upload_view(request):
    """
    Uploads a file and send back its URL to PAGEDOWN editor.

    TODO:
        Validate uploads
    """
    # Get the uploaded file from request.
    upload = request.FILES['file']

    # Open output file in which to store upload.
    upload_filename = get_upload_filename(upload.name, request.user)
    saved_path = default_storage.save(upload_filename, upload)


    url = default_storage.url(saved_path)
    # Respond with Javascript sending pagedown upload url.
    return JsonResponse({'success':True,'image_path':url})


