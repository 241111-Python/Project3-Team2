import pandas as pd
from geopy.geocoders import Nominatim
import ast
geoloc = Nominatim(user_agent='meteorite-causes.py')

#def findCountry(coor):
#    try:
#        loc = geoloc.reverse(coor, exactly_one=True, language='en', timeout=10)
#        ad = loc.raw['address']
#        (ad.get('country',''))
#        return ad.get('country','')
#    except:
#        return 'Ocean'
#
#meteors = pd.read_csv(r"maybeData\Meteorite_Landings.csv", usecols=['year', 'GeoLocation'])
#meteors.dropna(inplace=True)
#meteors = meteors[meteors['GeoLocation']!="(0.0, 0.0)"]
#meteors = meteors[meteors['year']>=1990]
#meteors['GeoLocation'] = meteors['GeoLocation'].apply(ast.literal_eval)
#meteors['GeoLocation'] = meteors['GeoLocation'].apply(findCountry)
#meteors.to_csv(r"maybeData\Meteorite_Countries.csv")


causes = pd.read_csv(r"maybeData\cause_of_deaths.csv")
causes.drop(['Code'], axis=1, inplace=True)
causes.rename(columns={'Country/Territory': "GeoLocation"}, inplace=True)
print(causes)
