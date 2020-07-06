import os
from settings import Hashtags, colors, interval_update, stop_words
# os.system('python3 data_collection.py')

# Dash libraries and components
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
from dash_table import DataTable

# Libraries working with data
import pandas as pd
import datetime
from sqlalchemy import create_engine


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUMEN])

server = app.server

engine = create_engine('sqlite:///server_db_1.db', echo=True)
query = 'SELECT Created_at, Text, Polarity FROM twitter_table ORDER BY Created_at DESC'
df = pd.read_sql_query(query, engine)

# Convert UTC into PDT
df['Created_at'] = pd.to_datetime(df['Created_at'])
df['Created_at'] = pd.to_datetime(df['Created_at']).apply(lambda x: x - datetime.timedelta(hours=7))

# Clean and transform data to enable time series
result = df.groupby([pd.Grouper(key='Created_at', freq='10s'), 'Polarity']).count().unstack(fill_value=0).stack().reset_index()
result = result.rename(
    columns={"id_str": "Num of '{}' mentions".format(Hashtags[0]), "Created_at": "Time"})
time_series = result["Time"][result['Polarity'] == 0].reset_index(drop=True)

min10 = datetime.datetime.now() - datetime.timedelta(hours=7, minutes=10)
min20 = datetime.datetime.now() - datetime.timedelta(hours=7, minutes=20)


app.layout = html.Div([
                     html.Div([
                         dcc.Graph(
                             id='crossfilter-indicator-scatter',
                             figure={
                                 'data': [
                                     go.Scatter(
                                         x=time_series,
                                         y=result["Num of '{}' mentions".format(Hashtags[0])][
                                             result['Polarity'] == 0].reset_index(drop=True),
                                         name="Neutrals",
                                         opacity=0.8,
                                         mode='lines',
                                         line=dict(width=0.5, color='rgb(131, 90, 241)'),
                                         stackgroup='one'
                                     ),
                                     go.Scatter(
                                         x=time_series,
                                         y=result["Num of '{}' mentions".format(Hashtags[0])][
                                             result['Polarity'] == -1].reset_index(drop=True).apply(lambda x: -x),
                                         name="Negatives",
                                         opacity=0.8,
                                         mode='lines',
                                         line=dict(width=0.5, color='rgb(255, 50, 50)'),
                                         stackgroup='two'
                                     ),
                                     go.Scatter(
                                         x=time_series,
                                         y=result["Num of '{}' mentions".format(Hashtags[0])][
                                             result['Polarity'] == 1].reset_index(drop=True),
                                         name="Positives",
                                         opacity=0.8,
                                         mode='lines',
                                         line=dict(width=0.5, color='rgb(184, 247, 212)'),
                                         stackgroup='three'
                                     )
                                 ]
                             }
                         )
                     ], style={'width': '73%', 'display': 'inline-block', 'padding': '0 0 0 20'})])

if __name__ == '__main__':
    app.run_server(debug=True)