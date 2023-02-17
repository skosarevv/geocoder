import io
import os

import requests
from PIL import Image

STATIC_API_SERVER = 'http://static-maps.yandex.ru/1.x/'


# https://yandex.ru/dev/maps/staticapi/doc/1.x/dg/concepts/markers.html
def get_marker_param(ll, style='pm2', color='wt', size='m', content=''):
    return f'pt={ll[0]},{ll[1]},{style}{color}{size}{content}'


def save_map(ll, spn=None, map_type='map', add_params=None):
    map_request = f'{STATIC_API_SERVER}?ll={ll[0]},{ll[1]}&l={map_type}{("&spn=" + spn) if spn is not None else ""}'
    if add_params:
        for param in add_params:
            map_request += '&' + param

    r = requests.get(map_request)
    i = Image.open(io.BytesIO(r.content))
    i.save(os.path.join('map.png'))


def show_map(path='map.png'):
    Image.open(path).show()
