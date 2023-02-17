import requests

GEOCODER_API_SERVER = 'http://geocode-maps.yandex.ru/1.x/'
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
