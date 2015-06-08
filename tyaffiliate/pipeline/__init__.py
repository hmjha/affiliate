from requests import request, ConnectionError
from django.core.files.base import ContentFile


def save_image(url, obj, filename):
    try:
        img_resp = request('GET', url)
        img_resp.raise_for_status()
    except ConnectionError:
        pass
    else:
        obj.image.save(filename,
                       ContentFile(img_resp.content),
                       save=False)
        obj.save()