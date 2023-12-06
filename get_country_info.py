

import pycountry
from restcountries import RestCountryApiV2 as rca

def get_land_area(iso_code):
    try:
        country = pycountry.countries.get(alpha_2=iso_code.upper())
        if country:
            country_name = country.name
            country_info = rca.get_countries_by_name(country_name)
            land_area = country_info[0].area if country_info else "Not available"
            return land_area
        else:
            return "Pfft"
    except Exception as e:
        return f"Error: {str(e)}"