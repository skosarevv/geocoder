import geocoder
import sys


# py 2.py Пермь, Самаркандская 102
toponym_to_find = " ".join(sys.argv[1:])
ll, spn = geocoder.get_toponym_ll_spn(toponym_to_find)
geocoder.save_map(ll, spn, add_params=geocoder.get_marker_param(ll, color='rd'))
geocoder.show_map()
