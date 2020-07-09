import os
from settings import Hashtags, colors, interval_update, stop_words, TABLE_COLS

# import figures
from figures.pie_chart_1 import  pie_sent
from figures.count_pie_2 import pie_count
from figures.scatter_plot_3 import scatter_plot
from figures.twit_table_4 import twit_table

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

# Libraries for Tokenization
import nltk
nltk.download('punkt')


#---------------------------------

# Libraries working with database
from sqlalchemy import create_engine

# Launch database Listener
engine = create_engine('sqlite:///server_db_1.db', echo=True)



app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUMEN])

server = app.server


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
                                'color': colors['txtcolor']}
                     ),
                     html.H4(
                         f'Currently listening on "{Hashtags[0]}"',
                         style={'text-align': 'center',
                                'color': colors['txtcolor']}
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
                        html.Br(),
                        html.P('Top-16 Words'),
                        dcc.Loading(dcc.Graph('count-pie'))

            ],
            style={'backgroundColor':colors['bgcolor'],
                   'text-align': 'center',
                   'padding': 5,
                   'padding-right': '5%',
                   'padding-left': '5%',
                   'margin': 5,
                   'border-radius': '5px',
                   'color': colors['txtcolor'],
                   'font-size': '24.5px'}),
            # Second Panel
            html.Div([
                    dbc.Col(lg=1),
                        html.Br(),
                        html.H3(
                            'Scatter Plot',
                            style={'text-align': 'center',
                                   'color': colors['txtcolor']},
                            className="control_label"
                        ),
                        # place for first figure
                        dcc.Graph(id='live-update-scatter'),
                        #place for second figure
                        html.H3('Twits Table',
                                style={'text-align': 'center',
                                       'color': colors['txtcolor']}
                                ),
                        # Twit Table
                        html.Div([DataTable(
                                            id='table',
                                            style_header={'textAlign': 'center',
                                                          'backgroundColor': colors['panelcolor']},
                                            style_cell={'font-family': 'Source Sans Pro',
                                                        # 'minWidth': '100%',
                                                        'maxWidth': 40,
                                                        'overflowX': 'auto',
                                                        'textOverflow': 'ellipsis',
                                                        'height': 'auto',
                                                        'font-size': 12,
                                                        'textAlign': 'left',
                                                        'color': colors['txtcolor'],
                                                        'backgroundColor': colors['bgcolor']},
                                            sort_action='native',
                                            columns=[{'name': i.title(), 'id': i}
                                                     for i in TABLE_COLS],
                                            style_data_conditional=[
                                                    {
                                                        'if': {
                                                            'filter_query': '{Polarity} > 0.2',
                                                            'column_id': 'Added_at'
                                                        },
                                                        'backgroundColor': '#3D9970',
                                                        'color': colors['txtcolor']
                                                    },
                                                    {
                                                        'if': {
                                                            'filter_query': '{Polarity} > 0.2',
                                                            'column_id': 'Text'
                                                        },
                                                        'backgroundColor': '#3D9970',
                                                        'color': colors['txtcolor']
                                                    },
                                                    {
                                                        'if': {
                                                            'filter_query': '{Polarity} > 0.2',
                                                            'column_id': 'Polarity'
                                                        },
                                                        'backgroundColor': '#3D9970',
                                                        'color': colors['txtcolor']
                                                    },

                                                {
                                                    'if': {
                                                        'filter_query': '{Polarity} < -0.2',
                                                        'column_id': 'Added_at'
                                                    },
                                                    'backgroundColor': '#FF4136',
                                                    'color': colors['txtcolor']
                                                },
                                                {
                                                    'if': {
                                                        'filter_query': '{Polarity} < -0.2',
                                                        'column_id': 'Text'
                                                    },
                                                    'backgroundColor': '#FF4136',
                                                    'color': colors['txtcolor']
                                                },
                                                {
                                                    'if': {
                                                        'filter_query': '{Polarity} < -0.2',
                                                        'column_id': 'Polarity'
                                                    },
                                                    'backgroundColor': '#FF4136',
                                                    'color': colors['txtcolor']
                                                }

                                            ],
                                            data=pd.DataFrame({
                                                k: ['' for i in range(10)] for k in TABLE_COLS}).to_dict('rows'),
                                        )],


                                 style={'display': 'center',
                                        'paddingLeft': '5%',
                                        'paddingRight': '10%',
                                        'paddingBottom': '2%',
                                        'border-radius': '5px'})


                    ],
                    style={'backgroundColor': colors['bgcolor'],
                           'margin': 5,
                           'border-radius': '5px',
                           'width': '71%'}),

            ],
            style={'paddingLeft': '3%'},
                 className='row'),

        html.Br(),
        dcc.Interval(
            id='interval-component-slow',
            interval=1 * interval_update,  # in milliseconds
            n_intervals=0)
    ],
    id="mainContainer",
    style={
        "display": "flex",
        "flex-direction": "column",
        'backgroundColor':'#051e3e'
    }
)


@app.callback([Output('sentiment-analysis', 'figure'),
               Output('count-pie', 'figure'),
               Output('live-update-scatter', 'figure')],
              [Input('interval-component-slow', 'n_intervals')])
def firstPanel(n_intervals):
    # Data Wrangling for Pie Chart
    query = 'SELECT Added_at, Text, Polarity FROM twitter_table ORDER BY Created_at DESC'
    df = pd.read_sql_query(query, engine)

    # first figure
    fig = pie_sent(df)

    # second figure
    fig_2 = pie_count(df)

    # Scatter Figure
    scatter = scatter_plot(df)

    return fig, fig_2, scatter


@app.callback(Output('table', 'data'),
              [Input('interval-component-slow', 'n_intervals')])
def sentimentable(n_intervals):
    # query for Table
    query = 'SELECT Added_at, Text, Polarity FROM twitter_table ORDER BY Added_at DESC'

    # Wrangling Table
    return twit_table(query, engine)

if __name__ == '__main__':
    app.run_server(debug=True, port='8800')

    # os.system('python3 data_collection.py')




