from datetime import datetime
from pprint import pprint
from urllib.parse import urlunparse, urlencode
from collections import OrderedDict
import requests

from django.conf import settings
from social_core.exceptions import AuthForbidden

from users.models import UserProfile


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

    api_url = urlunparse (('http', 'api.vk.com', '/method/users.get', None, urlencode(
        OrderedDict(fields=','.join(('bdate', 'sex', 'about', 'photo_max_orig', 'personal')),
                    access_token=response["access_token"], v=5.131)), None))

    resp = requests.get(api_url)
    if resp.status_code != 200:
        return
    pprint(resp.json())
    data = resp.json()['response'][0]

    if 'sex' in data:
        if data['sex'] == 1:
            user.userprofile.gender = UserProfile.FEMALE
        elif data['sex'] == 2:
            user.userprofile.gender = UserProfile.MALE

    if 'about' in data:
        user.userprofile.about_me = data['about']

    if 'bdate' in data:
        bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()
        age = datetime.now().year - bdate.year
        if age < 18:
            user.delete()
            raise AuthForbidden('social_core.backends.vk.VKOAuth2')
        user.age = age

    if 'langs' in data['personal']:
        user.userprofile.langs = ''
        for lang in data['personal']['langs']:
            user.userprofile.langs += f'{lang} '

    if 'photo_max_orig' in data:
        image_data = requests.get(data['photo_max_orig'])
        with open(f'{settings.MEDIA_ROOT}/users_images/{user.username}.jpg', 'wb') as f:
            f.write(image_data.content)
        user.image = f'/users_images/{user.username}.jpg'

    user.save()
