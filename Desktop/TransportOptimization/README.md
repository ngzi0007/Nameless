# Transport Optimization
Google OR-tools: https://developers.google.com/optimization/routing/pickup_delivery

To use: 
https://developers.google.com/maps/documentation/geocoding/intro  
https://developers.google.com/maps/documentation/distance-matrix/start  
## Requirements
Django
```bash
python -m pip install -U --user ortools
pip install dash-bootstrap-components
```
Create account at https://account.mapbox.com/, get access token, save it as text file ./data/mapbox_token.pk

Create account at https://developers.onemap.sg/signup/, get access token, save it as text file ./data/onemap_token.pk
Further Guide to Account registration can be foud here: https://discuss.onemap.sg/t/api-registration/60
```
Polyline Decoder
```bash
pip install polyline


## Quick Start
```bash
cd src/Django
./pre_run.sh
python manage.py runserver
```
