#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 14:14:48 2020

@author: nicholas
"""

import polyline
import requests
import plotly.graph_objects as go
import pandas as pd
import dash

fig=go.Figure()
app = dash.Dash(__name__)

#onemap API    
token_path = '../data/openmap_token.pk'
with open(token_path, 'r', encoding='utf8') as f:
    openMap_token = f.read().strip()

def route_decoder(start_lang,start_lon,end_lang,end_lon):
    
    # del_type is available in walk, bicycle and drive
    del_type= 'drive'
    url = 'https://developers.onemap.sg/privateapi/routingsvc/route?start='+start_lang+','+start_lon+'&end='+end_lang+','+end_lon+'&routeType='+del_type+'&token='+openMap_token
    response = requests.get(url)
    error_code = response.status_code
    if error_code == 200:
        # making the request a dictionary
        respo = response.json()
#       print(respo.get('route_geometry')) 
        coord = polyline.decode(respo.get('route_geometry'), 5)
#       print(coord)          #coord will be in a list
        
        lat_list = [tup[0] for tup in coord ]
        long_list = [tup[1] for tup in coord]
        start_lat_list = lat_list[:-1]
        end_lat_list = lat_list[1:]
        start_long_list = long_list[:-1]
        end_long_list = long_list[1:]
        
        # writing csv file for plotting
        csv_data = {'start_lat': start_lat_list, 'start_lon': start_long_list, 'end_lat': end_lat_list, 'end_lon': end_long_list}
        df = pd.DataFrame(csv_data,columns=['start_lat','start_lon','end_lat','end_lon'])
        print(df)

        df.to_csv ('export_dataframe.csv', header=True, index=False,mode='a')
  
    return 1
    
if __name__ == '__main__':
    route_decoder()
    app.run_server(debug=True)


