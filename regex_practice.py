__author__ = 'MilanAshara'

import skyscanner_id_to_iata

print skyscanner_id_to_iata.SKYSCANNER_TO_IATA_IDS.keys()


def get_funny_code(dict):
    funny_skyscanner_code = []
    for key in dict.keys():
        if not key.isalnum():
            funny_skyscanner_code.append(key)
    return funny_skyscanner_code

print get_funny_code(skyscanner_id_to_iata.SKYSCANNER_TO_IATA_IDS)
print set(get_funny_code(skyscanner_id_to_iata.SKYSCANNER_TO_AIRLINE_NAME))
print get_funny_code(skyscanner_id_to_iata.ICAO_IDS_TO_SKYSCANNER)
print get_funny_code(skyscanner_id_to_iata.IATA_IDS_TO_SKYSCANNER)

