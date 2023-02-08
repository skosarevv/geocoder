import io
import os
import requests
from PIL import Image

GEOCODER_API_SERVER = 'http://geocode-maps.yandex.ru/1.x/'
STATIC_API_SERVER = 'http://static-maps.yandex.ru/1.x/'
APIKEY = '40d1649f-0493-4b70-98ba-98533de7710b'


def get_ll(toponym_to_find) -> tuple:
    """Returns longitude and lattitude of toponym"""

    geocoder_params = {
        "apikey": APIKEY,
        "geocode": toponym_to_find,
        "format": "json"}

    response = requests.get(GEOCODER_API_SERVER, params=geocoder_params)

    if not response:
        print('ERROR', response.status_code)
        return

    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    toponym_coodrinates = toponym["Point"]["pos"]

    return tuple(toponym_coodrinates)


def get_toponym_ll_spn(toponym_to_find):
    """Returns longitude and lattitude of toponym"""

    geocoder_params = {
        "apikey": APIKEY,
        "geocode": toponym_to_find,
        "format": "json"}

    response = requests.get(GEOCODER_API_SERVER, params=geocoder_params)

    if not response:
        print('ERROR', response.status_code)
        return

    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    toponym_coodrinates = toponym["Point"]["pos"]
    lo, la = toponym_coodrinates.split(' ')
    ll = tuple([lo, la])

    envelope = toponym['boundedBy']['Envelope']
    left, bottom = envelope['lowerCorner'].split(' ')
    right, top = envelope['upperCorner'].split(' ')
    dx = abs(float(right) - float(left)) / 2
    dy = abs(float(bottom) - float(top)) / 2
    spn = ','.join([str(dx), str(dy)])

    return ll, spn


def save_map(ll, spn=None, map_type='map', add_params=None):
    map_request = f'{STATIC_API_SERVER}?ll={ll[0]},{ll[1]}&l={map_type}{("&spn=" + spn) if spn is not None else ""}'
    if add_params:
        for param in add_params:
            map_request += '&' + param

    r = requests.get(map_request)
    i = Image.open(io.BytesIO(r.content))
    i.save(os.path.join('map.png'))


# https://yandex.ru/dev/maps/staticapi/doc/1.x/dg/concepts/markers.html
def get_marker_param(ll, style='pm2', color='wt', size='m', content=''):
    return f'pt={ll[0]},{ll[1]},{style}{color}{size}{content}'


def show_map(path='map.png'):
    Image.open(path).show()
