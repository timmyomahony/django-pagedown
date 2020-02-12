import os
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
from django.core.files.storage import default_storage


IMAGE_UPLOAD_EXTENSIONS = getattr(settings, 'PAGEDOWN_IMAGE_UPLOAD_EXTENSIONS', [
    '.jpg',
    '.jpeg',
    '.png',
    '.svg',
    '.webp'
])
IMAGE_UPLOAD_MAX_SIZE = getattr(
    settings, 'PAGEDOWN_IMAGE_UPLOAD_MAX_SIZE', 20 * 1024 * 1024)
IMAGE_UPLOAD_PATH = getattr(
    settings, 'PAGEDOWN_IMAGE_UPLOAD_PATH', 'pagedown-uploads')


@login_required
@csrf_exempt
def image_upload_view(request):
    file = request.FILES['file']
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Method not allowed'})
    if not file:
        return JsonResponse({'success': False, 'error': 'No file found'})
    if not any([file.name.endswith(e) for e in IMAGE_UPLOAD_EXTENSIONS]):
        return JsonResponse({'success': False, 'error': 'Invalid extension'})
    if file.size > IMAGE_UPLOAD_MAX_SIZE:
        return JsonResponse({'success': False, 'error': 'File too large'})
    path = os.path.join(IMAGE_UPLOAD_PATH, file.name)
    path = default_storage.save(path, file)
    url = default_storage.url(path)
    return JsonResponse({'success': True, 'url': url})
