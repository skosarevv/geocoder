import geocoder
import sys

import staticapi

# py 2.py Пермь, Самаркандская 102
toponym_to_find = " ".join(sys.argv[1:])
ll, spn = geocoder.get_toponym_ll_spn(toponym_to_find)
staticapi.save_map(ll, spn, add_params=staticapi.get_marker_param(ll, color='rd'))
staticapi.show_map()
