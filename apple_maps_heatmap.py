import requests
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go


url = "https://covid19-static.cdn-apple.com/covid19-mobility-data/2008HotfixDev42/v3/en-us/applemobilitytrends-2020-05-24.csv"

r = requests.get(url)
url_content = r.content
csv_file = open('am_downloaded.csv', 'wb')
csv_file.write(url_content)
csv_file.close()
file_folder = '/Users/rosleeb/ny_thruway'
data = pd.read_csv(f'{file_folder}/am_downloaded.csv')

data["Map"] = data["region"] + "_" + data["transportation_type"]
data = data.drop(['geo_type','alternative_name','region','transportation_type', 'sub-region', "country"], axis=1)
maps = data['Map']
data.drop(labels=['Map'], axis=1,inplace = True)
data.insert(0, 'Map', maps)
data = data.set_index('Map')
data = pd.DataFrame(data.T)

states = ['Alabama_driving', 'Alaska_driving', 'Arizona_driving', 'Arkansas_driving', 
          'California_driving', 'Colorado_driving', 'Connecticut_driving', 'Delaware_driving',
         'Florida_driving', 'Georgia_driving', 'Hawaii_driving', 'Idaho_driving', 'Illinois_driving',
         'Indiana_driving','Iowa_driving', 'Kansas_driving', 'Kentucky_driving', 'Louisiana_driving',
         'Maine_driving', 'Maryland_driving', 'Massachusetts_driving', 'Michigan_driving', 'Minnesota_driving',
         'Mississippi_driving', 'Missouri_driving', 'Montana_driving', 'Nebraska_driving', 'Nevada_driving',
         'New Hampshire_driving', 'New Jersey_driving', 'New Mexico_driving', 'New York_driving', 'North Dakota_driving',
         'North Carolina_driving', 'Ohio_driving', 'Oklahoma_driving', 'Oregon_driving', 'Pennsylvania_driving',
         'Rhode Island_driving', 'South Carolina_driving', 'South Dakota_driving', 'Tennessee_driving',
         'Texas_driving', 'Utah_driving', 'Vermont_driving', 'Virginia_driving', 'Washington_driving',
         'West Virginia_driving', 'Wisconsin_driving', 'Wyoming_driving']

state_codes = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE','FL', 'GA', 'HI', 'ID', 'IL',
         'IN','IA', 'KS', 'KY', 'LA','ME', 'MD', 'MA', 'MI', 'MN','MS', 'MO', 'MT', 'NE', 'NV',
         'NH', 'NJ', 'NM', 'NY', 'ND','NC', 'OH', 'OK', 'OR', 'PA','RI', 'SC', 'SD', 'TN',
         'TX', 'UT', 'VT', 'VA', 'WA','WV', 'WI', 'WY']

heat_map = []
for i in range(len(states)):
    #heat_map.append([states[i][:-8], data[states[i]][-1]])
    heat_map.append([state_codes[i], data[states[i]][-1]])

heat_map = pd.DataFrame(heat_map)
heat_map.columns = ['State', "Mobility"]

fig = go.Figure(data=go.Choropleth(
    locations=heat_map['State'], # Spatial coordinates
    z = heat_map['Mobility'], # Data to be color-coded
    locationmode = 'USA-states', # set of locations match entries in `locations`
    colorscale = 'Greens',
    colorbar_title = "Mobility Index",
))

fig.update_layout(
    title_text = 'Apple Maps Mobility Index',
    geo_scope='usa', # limite map scope to USA
)

fig.show()