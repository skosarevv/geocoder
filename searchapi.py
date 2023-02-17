import requests

SEARCH_API_SERVER = "https://search-maps.yandex.ru/v1/"
API_KEY = 'dda3ddba-c9ea-4ead-9010-f43fbc15c6e3'


def search(text: str, address_ll: tuple = None, spn=None, type=None, results=1) -> list:
    search_params = {
        "apikey": API_KEY,
        "text": text,
        "lang": "ru_RU",
        "type": "biz",
        'results': results
    }
    if address_ll:
        search_params['ll'] = address_ll
    if spn:
        search_params['spn'] = spn
    if type:
        search_params['type'] = type

    response = requests.get(SEARCH_API_SERVER, params=search_params)
    if not response:
        raise RuntimeError

    json_response = response.json()

    organisations = []
    for i in range(results):
        # Получаем первую найденную организацию.
        organization = json_response["features"][0]
        org_name = organization["properties"]["CompanyMetaData"]["name"]
        org_address = organization["properties"]["CompanyMetaData"]["address"]

        point = organization["geometry"]["coordinates"]
        org_ll = (point[0], point[1])

        organisations.append((org_name, org_address, org_ll))

    return organisations
