from flask import Flask, render_template
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
    

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the list of ISO codes from the form
        iso_codes = request.form.getlist('iso_codes')

        # Call the Python function for each ISO code and store the results
        results = {iso_code: get_land_area(iso_code) for iso_code in iso_codes}

        return render_template('index.html', results=results)

    return render_template('index.html', results=None)

if __name__ == '__main__':
    app.run(debug=True)