#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 12:23:34 2020

@author: weetee
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import plotly.graph_objects as go
import requests
import json
import polyline     #neend to 'pip install poluline'
import plotly.graph_objects as go
import pandas as pd


from params import DataModel
from solver import main_solver

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config['suppress_callback_exceptions'] = False


# Navbar
from navbar import Navbar as navbar
from API_openmap_route import route_decoder

#css stylings
styles = {'pre': {'border': 'thin lightgrey solid','overflowX': 'scroll'}}
logo_img = 'https://pngimage.net/wp-content/uploads/2018/06/imda-logo-png.png'

### define map
token_path = '../data/mapbox_token.pk'
with open(token_path, 'r', encoding='utf8') as f:
    mapbox_access_token = f.read().strip()

#onemap API    
token_path = '../data/openmap_token.pk'
with open(token_path, 'r', encoding='utf8') as f:
    openMap_token = f.read().strip()


fig = go.Figure()

# Global Variables
coordinate_input = '''(1.416221, 103.870980),
(1.382944, 103.893372),
(1.359355, 103.886654),
(1.352877, 103.877846),
(1.343985, 103.872836),
(1.445750, 103.783694),
(1.398481, 103.746880),
(1.306487, 103.850675),
(1.303979, 103.831849),
(1.293550, 103.784404)'''


### define HTML template
app.layout = html.Div(children =[
            html.Div(children =[
                    navbar(),
                    ]),
        html.Div(children =[
            html.Div([
                    dcc.Graph(
                            id='sg_map',
                            figure=dict(
                                    data=[],
                                    layout={},),
                            ),
                    html.Hr(),
                  
                    ], style = {'width':'55%'}),
            html.Div([                
                    html.Br(),html.Br(),
                    html.Div(children = [html.Div("Input the address / postal code of interest"),
        #                                 dbc.Input(id="input_address"),
                                         dbc.Input(id="postal_code", type="number")]),            
                    html.Button(id='submit_btn', children=['Submit address']),        
                    html.Div(id='print_address'),
                    html.Div(id='print_coordinates'),
                    html.Div(id='print_status'),
#                    html.Div(children = [coordinate_input]),
                    
                    html.Label('Input locations coordinates:', style={"font-weight": "bold"}),
                    html.Br(),
#                    html.Div(coordinate_input),
                    dcc.Textarea(
                        id='loc_coords',
                        value= coordinate_input, # placeholder
                        rows=5,
                        contentEditable = False,
                        style={'display': 'inline-block', 'verticalAlign': 'top', 'width': '70%'},
                    ),
                    html.Button('Show on map',
                                id='show_map',
                                n_clicks=0
                                ),
                            
                    html.Hr(),
                    html.Label('Input pickup-deliveries location ids:', style={"font-weight": "bold"}),\
                    html.Br(),
                    dcc.Textarea(
                        id='pickups_deliveries',
                        value='''[1, 5],\n[2, 6],\n[3, 7],\n[4, 8],''',
                        rows=5,
                        style={'display': 'inline-block', 'verticalAlign': 'top', 'width': '70%'},
                    ),
                   
                    html.Hr(),
                    html.Label('Input number of vehicles:', style={"font-weight": "bold"}),
                    html.Br(),
                    dcc.Input(id='n_vehicles', value='4', type='text', style={ 'width': '70%'}),
                    html.Button('Get Routes',
                                id='input-on-submit',
                                n_clicks=0
                                ),                             

                    html.Hr(),
                    html.Div( children=[
                            html.Label('Calculated routes:', style={"font-weight": "bold", "border":"2px black solid"}),
                            html.Br(),
                            #html.Div(id='route_output',)
                            dcc.Textarea(
                                id='route_output',
                                placeholder='''''',
                                rows=5,
                                style={'display': 'inline-block', 'verticalAlign': 'top','width':'75%'},
                                readOnly=True
                            )], style = {'margin':'0%,0%,0%,0px'})                     
                    

                    ], style = {'width':'35%'}),
         ], style = {'display':'flex','height':'55%'})
        ])    

@app.callback(

    [Output('print_address','children'),
     Output('print_coordinates','children'),
     Output('loc_coords', 'value')],
    [Input('submit_btn','n_clicks')],
    [State('postal_code','value')]
)
def address_to_coordinates(n_clicks, venue):
    global coordinate_input
    
    if n_clicks:
            venue = str(venue)
            url = 'https://developers.onemap.sg/commonapi/search?searchVal='+venue+'&returnGeom=Y&getAddrDetails=Y&pageNum=1'
            response = requests.get(url)
            error_code = response.status_code
            if error_code == 200:
                # making the request a dictionary
                respo = response.json()
        
                if respo['found'] >=1:
                    # taking the list from the dictionary
                    results = respo['results']
                    # taking the first value to get the respective coordinates
                    latitude = results[0]["LATITUDE"]
                    longitude = results[0]["LONGITUDE"]
                    coordinate = ',\n('+ latitude +', ' + longitude + ')'
                    # for global dictionary
                    coordinate_input+= coordinate
                    print(coordinate_input)
                    #print the full list to ensure the item taken is accurate
                    print(results[0])
                    return results[0]['SEARCHVAL'], coordinate , coordinate_input
                    
                else:
                    se = 'No such place available, Please try again' 
                    return se, None , None
            
            elif error_code == 404:
                print('Awesome, error with the URL input')
                se = 'URL not available available, Please try again' 
                return se, None , None
            else:
                print('Some unknown error')    
                se = 'URL not available available, Please try again' 
                return se, None , None                
        
    else: 
        raise PreventUpdate
    
    
    

@app.callback(
    Output(component_id='sg_map', component_property='figure'),
    [Input('show_map', 'n_clicks')],
    [State(component_id='loc_coords', component_property='value')]
)
def show_on_map(n_clicks, loc_coords):
    loc_coords = str(loc_coords)
    loc_coords_ = eval('[' + loc_coords.replace('\n', '') + ']')
    lats = [l for l, _ in loc_coords_]
    longs = [l for _, l in loc_coords_]
     
    #setting up orginal map                     
    fig = go.Figure(go.Scattermapbox(
            lat=lats,
            lon=longs,
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=14
            ),
            text=['p' for _ in range(len(lats))],
        ))
    
    #plotting of waypoints and rescale 
    df_paths = pd.read_csv('export_dataframe.csv')

    for i in range(len(df_paths)):
        if i%10 ==0: 
            fig.add_trace(
                go.Scattermapbox(
                    lon = [df_paths['start_lon'].iloc[i], df_paths['end_lon'].iloc[i]],
                    lat = [df_paths['start_lat'].iloc[i], df_paths['end_lat'].iloc[i]],
                    mode = 'lines',
                    line = dict(width = 2,color = 'red'),
                )
            )
            
    fig.update_layout(
        hovermode='closest',
        width=1000,
        height=700,
        mapbox=dict(
            accesstoken=mapbox_access_token,
            bearing=0,
            center=go.layout.mapbox.Center(
                lat=1.340270,
                lon=103.811959
            ),
            pitch=0,
            zoom=10.2
        ),
    ),
    return fig

@app.callback(
    Output(component_id='route_output', component_property='value'),
    [Input('input-on-submit', 'n_clicks')],
    state=[State(component_id='loc_coords', component_property='value'),\
     State(component_id='pickups_deliveries', component_property='value'),\
     State(component_id='n_vehicles', component_property='value')],\
)
def update_route(n_clicks, loc_coords, pickups_deliveries, n_vehicles):
    loc_coords_ = eval('[' + loc_coords.replace('\n', '') + ']')
    loc_names_ = ['loc_%d' % i for i in range(len(loc_coords_))]
    pickups_deliveries_ = eval('[' + pickups_deliveries.replace('\n', '') + ']')
    #sends all data into params.py for processing
    n_vehicles_ = int(n_vehicles)
    dm = DataModel(order_locs=loc_coords_,\
                   order_locs_names=loc_names_,\
                   pickups_deliveries=pickups_deliveries_,\
                   num_vehicles=n_vehicles_)
    # plan_outputs print the route on the dashboard. route solution isa dict with route_soln[vehicle_id] = route_path
    route_soln, plan_outputs = main_solver(data=dm.data)
    print(route_soln)

    for vehicle_id in route_soln:
        #shows you the current loop for which vehicle id
        print(route_soln[vehicle_id])
        #formation of waypoints based on coordinates
        for route_index in route_soln[vehicle_id]:
            start_lan, start_lon = dm.order_locs[route_index - 1]
            end_lan, end_lon = dm.order_locs[route_index]
            print('start lan')
            print(start_lan + start_lon)
            print('end lon')
            print(end_lan + end_lon)
            route_decoder(str(start_lan),str(start_lon),str(end_lan),str(end_lon))
               
    return plan_outputs


if __name__ == '__main__':
    app.run_server(debug=True,port=8555)