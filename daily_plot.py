# -*- coding: utf-8 -*-
"""
Created on Sun Mar 18 15:40:37 2018

@author: divyadeep
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input
from dash.dependencies import Output
import plotly.graph_objs as go

import pandas as pd

df = pd.read_csv('dst_data.csv')

years = sorted(df['Year'].unique())
months = range(1, 13)
hours_columns = [hour for hour in df.columns if hour not in ['Year', 'Month', 'Day']]
hours = pd.Series(range(0,24))

app = dash.Dash()

app.layout = html.Div([
    html.H1('Daily DST index graph.'),
    dcc.Dropdown(
        id = 'year',
        options = [
            {'label' : i, 'value' : i} for i in years
        ],
        placeholder = 'Select an year',
        value = 1957
    ),
    dcc.Dropdown(
        id = 'month',
        options = [
            {'label' : i, 'value' : i} for i in months
        ],
        placeholder = 'Select a month',
        value = 1
    ),
    dcc.Graph(
        id = 'daily_graph',    
    ),
    html.Label('Slider'),
    dcc.Slider(
        id = 'day',
        min = 1
    ),
])

@app.callback(
    Output('day', 'max'),
    [Input('month', 'value'),
     Input('year', 'value')]
)
def update_slider_max_value(month, year):
    if month==2 and year%4==0:
        return 29
    elif month==2 and year%4!=0:
        return 29
    elif month in [4,6,9,11]:
        return 30
    else:
        return 31

@app.callback(
    Output('day', 'marks'),
    [Input('month', 'value'),
     Input('year', 'value')]
)
def update_slider_marks(month, year):
    if month==2 and year%4==0:
        return {i: i for i in range(1, 30)}
    elif month==2 and year%4!=0:
        return {i: i for i in range(1, 29)}
    elif month in [4,6,9,11]:
        return {i: i for i in range(1, 31)}
    else:
        return {i: i for i in range(1, 32)}

@app.callback(
    Output(component_id='daily_graph', component_property='figure'),
    [Input(component_id='year', component_property='value'),
    Input(component_id='month', component_property='value'),
    Input(component_id='day', component_property='value')]
)
def update_graph(year, month, day):
    data = df[(df['Year']==year) & (df['Month']==month) & (df['Day']==day)]
    hour_dst_data = pd.Series(data[hours_columns].iloc[0].values)
    print(hour_dst_data)
    graph_data = go.Scatter(
        x = hours,
        y = hour_dst_data,
        mode = 'markers',
        opacity = 1,
        marker={
            'size' : 15,
            'line' : {'width' : 0.5, 'color' : 'blue'}
        }
    )
    return{
        'data' : [graph_data],
        'layout' : go.Layout(
            xaxis = {'title' : 'Time of day'},
            yaxis = {'title' : 'DST index', 'range' : [min(hour_dst_data)-1, max(hour_dst_data)+1]},
            margin = {'l' : 40, 'r' : 20, 't' : 20, 'b' : 20},
            legend = {'x' : 0, 'y' : 1},
            hovermode = 'closest'
        )
    }
    
    
    

if __name__ == '__main__':
    app.run_server(debug=True)