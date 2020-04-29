#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 09:51:41 2020

@author: nicholas
"""
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html

def Navbar():
     navbar = dbc.NavbarSimple(
           children=[
#              dbc.NavItem(dbc.NavLink("EA Dashboard", href="/Energy_Analytics")),
#              dbc.NavItem(dbc.NavLink("Energy Prediction", href="/Energy_Prediction")),
              dbc.DropdownMenu(
                 nav=True,
                 in_navbar=True,
                 label="Menu",
                 children=[
                    dbc.DropdownMenuItem("Entry 1"),
                    dbc.DropdownMenuItem("Entry 2"),
                    dbc.DropdownMenuItem(divider=True),
                    dbc.DropdownMenuItem("Entry 3"),
                          ],
                      ),
                    ],
          brand="Home",
          brand_href="/home",
          sticky="top",
          color='dark',
          dark = True,
          style = {"background-color" : '#aaa'}
        )
     return navbar
 

