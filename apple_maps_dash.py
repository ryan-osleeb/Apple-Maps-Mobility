import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html

#url = "https://covid19-static.cdn-apple.com/covid19-mobility-data/2009HotfixDev22/v3/en-us/applemobilitytrends-2020-06-06.csv"
#url = "https://covid19-static.cdn-apple.com/covid19-mobility-data/2010HotfixDev17/v3/en-us/applemobilitytrends-2020-06-13.csv"
#url = "https://covid19-static.cdn-apple.com/covid19-mobility-data/2010HotfixDev25/v3/en-us/applemobilitytrends-2020-06-20.csv"

#r = requests.get(url)
#url_content = r.content
#csv_file = open('am_downloaded.csv', 'wb')
#csv_file.write(url_content)
#csv_file.close()
#file_folder = '/Users/rosleeb/ny_thruway'
#data = pd.read_csv(f'{file_folder}/am_downloaded.csv')
data = pd.read_csv('am_downloaded.csv')


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
    #heat_map.append([state_codes[i], np.average(data[states[i]][-7:])])
    heat_map.append([state_codes[i], np.average(data[states[i]][-7:])-np.average(data[states[i]][-14:-7])])

heat_map = pd.DataFrame(heat_map)
heat_map.columns = ['State', "Mobility"]

US_driving = np.array(data['United States_driving'])
US_walking = np.array(data['United States_walking'])
US_transit = np.array(data['United States_transit'])

Arizona = np.array(data['Arizona_driving'])
California = np.array(data['California_driving'])
Florida = np.array(data['Florida_driving'])
Texas = np.array(data['Texas_driving'])

us_driving = go.Scatter(
                x = data.index,
                y = US_driving,
                name = 'US Driving',
                mode = 'lines'
    )

us_walking = go.Scatter(
                x = data.index,
                y = US_walking,
                name = 'US Walking',
                mode = 'lines'
    )

us_transit = go.Scatter(
                x = data.index,
                y = US_transit,
                name = 'US Transit',
                mode = 'lines'
    )

AZ_mobility = go.Scatter(
                x = data.index,
                y = Arizona,
                name = 'Arizona',
                mode = 'lines'
    )

CA_mobility = go.Scatter(
                x = data.index,
                y = California,
                name = 'California',
                mode = 'lines'
    )

FL_mobility = go.Scatter(
                x = data.index,
                y = Florida,
                name = 'Florida',
                mode = 'lines'
    )

TX_mobility = go.Scatter(
                x = data.index,
                y = Texas,
                name = 'Texas',
                mode = 'lines'
    )

US_data = [us_driving, us_walking, us_transit]
Risk_data = [AZ_mobility, CA_mobility, FL_mobility, TX_mobility]

fig1 = go.Figure(data = US_data)

fig1.update_layout(
     title_text = 'Apple Maps Mobility Index',
 )

fig2 = go.Figure(data = Risk_data)

fig2.update_layout(
     title_text = 'Apple Maps Mobility Driving States At-Risk',
 )

fig3 = go.Figure(data=go.Choropleth(
    locations=heat_map['State'], # Spatial coordinates
    z = heat_map['Mobility'], # Data to be color-coded
    locationmode = 'USA-states', # set of locations match entries in `locations`
    colorscale = 'Greens',
    colorbar_title = "Mobility Index",
))

fig3.update_layout(
    title_text = 'Apple Maps Mobility Heat Map',
    geo_scope='usa', # limite map scope to USA
)

app = dash.Dash(__name__)

app.layout = html.Div(children=[html.H1(children=''),
                        dcc.Graph(
                                id = 'US Driving',
                                figure=fig1
                            ),
                        html.H2(children=''),
                        dcc.Graph(
                                id = 'At Risk States',
                                figure=fig2
                            ),
                        html.H3(children=''),
                        dcc.Graph(
                                id = 'US Heat Map',
                                figure=fig3
                            )
                            ])

if __name__ == '__main__':
    app.run_server(debug=True)
