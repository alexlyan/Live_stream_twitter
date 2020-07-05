import os
from settings import Hashtags
# os.system('python3 data_collection.py')

# Dash libraries and components
import dash
import dash_bootstrap_components as dbc
import plotly.express as px
from dash.exceptions import PreventUpdate
from dash_table import DataTable
import dash_html_components as html
import dash_core_components as dcc
from plotly import express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from dash_table.FormatTemplate import Format
from dash.dependencies import Input, Output, State

# Libraries working with data
from textblob import TextBlob
from datetime import datetime
import re
import pandas as pd
import numpy as np
import os

# Libraries working with database
from sqlalchemy import create_engine

# Launch database Listener

engine = create_engine('sqlite:///server_db_1.db', echo=True)
query = 'SELECT * FROM twitter_table'

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUMEN])

server = app.server

# Values for testing
labels = ['Oxygen','Hydrogen','Carbon_Dioxide','Nitrogen']
values = [4500, 2500, 1053, 500]
figure = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.5, showlegend =False)], layout={'height': 280,
                                                                                                    'margin': {'l': 0,
                                                                                                               'r': 0,
                                                                                                               'b': 50,
                                                                                                               't':0}})
figure.update_layout(plot_bgcolor = '#173F5F', paper_bgcolor='#173F5F')
#

app.layout = html.Div(
    [
        # header
        dbc.Row(
            [
             dbc.Col(
                 [html.Br(),
                     html.H2(
                         'Twitter Streamer',
                         style={'text-align': 'center',
                                'color': '#e7eff6 '}
                     ),
                     html.H4(
                         f'Currently listening on "{Hashtags[0]}"',
                         style={'text-align': 'center',
                                'color': '#e7eff6 '}
                     )
                 ]
             )
             ],
            id='header',
            className='row'),

        html.Div([
            # Pie chart and table
            html.Div([
                    dbc.Col(lg=1),
                        html.Br(),
                        html.P(
                            'Sentiment Analysis'
                        ),
                        # Pie chart with sentiment analysis
                        dcc.Graph('sentiment-analysis'),
                        # Table with last twits
                        dcc.Graph(figure=figure)

            ],
            style={'backgroundColor': '#173F5F',
                   'padding': 5,
                   'padding-right': '5%',
                   'padding-left': '5%',
                   'margin': 5,
                   'border-radius': '5px',
                   'color': '#e7eff6',
                   'font-size': '24.5px'}),
            # Second Panel
            html.Div([
                    dbc.Col(lg=1),
                        html.Br(),
                        html.H3(
                            'Sound Chart',
                            style={'text-align': 'center',
                                   'color': '#e7eff6'},
                            className="control_label"
                        ),
                        # place for first figure
                        dcc.Graph(figure=figure),
                        #place for second figure
                        html.H3('Count Histogram',
                                style={'text-align': 'center',
                                       'color': '#e7eff6'}
                                ),
                        dcc.Graph(figure=figure)

                    ],
                    style={'backgroundColor': '#173F5F',
                           'margin': 5,
                           'border-radius': '5px',
                           'width': '71%'}),

            ],
            style={'paddingLeft': '3%'},
                 className='row'),

        html.Br(),
        dcc.Interval(
            id='interval-component-slow',
            interval=1 * 10000,  # in milliseconds
            n_intervals=0)
    ],
    id="mainContainer",
    style={
        "display": "flex",
        "flex-direction": "column",
        'backgroundColor':'#051e3e'
    }
)


@app.callback(Output('sentiment-analysis', 'figure'),
              [Input('interval-component-slow', 'n_intervals')])
def firstPanel(n_intervals):

    df = pd.read_sql_query(query, engine)
    sentiment_list = []
    # neutral
    sentiment_list.append(len(df[(df['Polarity'] >= -0.4) & (df['Polarity'] <= 0.4)]))
    # negative
    sentiment_list.append(sum(df['Polarity'] < -0.4))
    # Positive
    sentiment_list.append(sum(df['Polarity'] > 0.4))

    labels = ['Neutral', 'Negative', 'Positive']
    values = sentiment_list
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.5, showlegend=False)], layout={'height': 280,
                                                                                                    'margin': {'l': 0,
                                                                                                               'r': 0,
                                                                                                               'b': 50,
                                                                                                               't':0}})
    fig.update_layout(plot_bgcolor='#173F5F', paper_bgcolor='#173F5F')

    return fig

if __name__ == '__main__':
    # os.system('python3 data_collection.py')
    app.run_server(debug=True, port='8800')




