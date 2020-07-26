# -*- coding: utf8 -*-
"""
@author: Ahmad.Hussein
"""
import pandas as pd
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output


# start the app 
app = dash.Dash(__name__)
# ----------------------------------------------------------
# import the data and clean it
df = pd.read_csv('intro_bees.csv')

df = df.groupby(['State', 'ANSI', 'Affected by', 'Year', 'state_code'])[['Pct of Colonies Impacted']].mean()
df.reset_index(inplace = True)
# ------------------------------------------------------------

# app layout
app.layout= html.Div([
        
html.H1("Web Application Dashboards with Dash", style = {'text-align' : 'center'}),

dcc.Dropdown(id = 'slct_year',
             # label is what the user sees
             # value should be in the same format as you r dataframe
             options = [{'label' : '2015', 'value' : 2015},
                        {'label' : '2016', 'value' : 2016},
                        {'label' : '2017', 'value' : 2017},
                        {'label' : '2018', 'value' : 2018}],
                        multi = False,
                        #initially
                        value = 2015,
                        style = {'width' : '40%'}),
             
# add the choropelth map
dcc.Graph(id = 'map')

])

# -------------------------------------------------------
# app callbacks
# define the outputs for this callback function 
@app.callback(
    Output(component_id='map', component_property='figure'),
    [Input(component_id='slct_year', component_property='value')]
)
# function for the call back above, used to actually output to the outputs defined in the callback
def update_figure(option_selected):
    print(option_selected)
    
    # create the fig based on the option selected and return it
    
    #play around with the copy
    df_copy = df.copy()
    print(df_copy)

    df_copy = df_copy[df_copy['Year'] == option_selected]
    
    print(df_copy)
    
    data = dict(
            type = 'choropleth',
            locations = df_copy['state_code'],
            locationmode = 'USA-states',
            z = df_copy['Pct of Colonies Impacted'],
            colorscale = 'Portland',
            colorbar_title = 'Percentage of Colonies')
    
    layout = dict(title_text = 'Bees', geo = dict(scope = 'usa'))
    
    fig = go.Figure(data = [data], layout = layout)
    
    return fig
#
if __name__ == '__main__':
    app.run_server(debug = False)