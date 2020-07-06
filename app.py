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

# Libraries for Tokenization

import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize


#---------------------------------

# Libraries working with database
from sqlalchemy import create_engine

# Launch database Listener
engine = create_engine('sqlite:///server_db_1.db', echo=True)

TABLE_COLS = ['Created_at', 'Text', 'Polarity']

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUMEN])

server = app.server

# Values for testing
labels = ['Oxygen','Hydrogen','Carbon_Dioxide','Nitrogen']
values = [4500, 2500, 1053, 500]
figure = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.5, showlegend =False)],
                   layout={'height': 280,
                            'margin': {'l': 0,
                                       'r': 0,
                                       'b': 50,
                                       't':0}})

figure.update_layout(plot_bgcolor = colors['bgcolor'],
                     paper_bgcolor=colors['bgcolor'])
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
                        # dcc.Graph(figure=figure)
                        # Sunburst of words
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
                        dcc.Graph(figure=figure),
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
                                                        'overflow': 'hidden',
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
                                                            'filter_query': '{Polarity} > 0.4',
                                                            'column_id': 'Created_at'
                                                        },
                                                        'backgroundColor': '#3D9970',
                                                        'color': colors['txtcolor']
                                                    },
                                                    {
                                                        'if': {
                                                            'filter_query': '{Polarity} > 0.4',
                                                            'column_id': 'Text'
                                                        },
                                                        'backgroundColor': '#3D9970',
                                                        'color': colors['txtcolor']
                                                    },
                                                    {
                                                        'if': {
                                                            'filter_query': '{Polarity} > 0.4',
                                                            'column_id': 'Polarity'
                                                        },
                                                        'backgroundColor': '#3D9970',
                                                        'color': colors['txtcolor']
                                                    },

                                                {
                                                    'if': {
                                                        'filter_query': '{Polarity} < -0.4',
                                                        'column_id': 'Created_at'
                                                    },
                                                    'backgroundColor': '#FF4136',
                                                    'color': colors['txtcolor']
                                                },
                                                {
                                                    'if': {
                                                        'filter_query': '{Polarity} < -0.4',
                                                        'column_id': 'Text'
                                                    },
                                                    'backgroundColor': '#FF4136',
                                                    'color': colors['txtcolor']
                                                },
                                                {
                                                    'if': {
                                                        'filter_query': '{Polarity} < -0.4',
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


@app.callback(Output('sentiment-analysis', 'figure'),
              [Input('interval-component-slow', 'n_intervals')])
def firstPanel(n_intervals):
    # Data Wrangling for Pie Chart
    query = 'SELECT Created_at, Polarity FROM twitter_table ORDER BY Created_at DESC'
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
    fig = go.Figure(data=[go.Pie(labels=labels,
                                 values=values,
                                 hole=0.5,
                                 showlegend=False,
                                 marker= dict(colors=['#0080ff', '#FF6792', '#725EB7']))],
                    layout={'height': 260,
                            'margin': {'l': 0,
                                       'r': 0,
                                       'b': 0,
                                       't':0}})
    fig.update_layout(plot_bgcolor=colors['bgcolor'], paper_bgcolor=colors['bgcolor'],
                      annotations=[dict(visible=True,
                                        font_color='white',
                                        text=f'{len(df)/1000:.2f}K',
                                        x=0.55,
                                        y=0.37,
                                        font_size=20,
                                        showarrow=True)])

    return fig


@app.callback(Output('count-pie', 'figure'),
              [Input('interval-component-slow', 'n_intervals')])
def countPie(n_intervals):
    # Data Wrangling for Pie Chart
    query = 'SELECT Text FROM twitter_table'
    df = pd.read_sql_query(query, engine)

    # Clean text from garbage word
    content = ' '.join(list(map(lambda x: x if x != None else '', list(df['Text']))))

    # Tokenization
    tokenized_word = word_tokenize(content)
    # stop_words = set(stopwords.words("english"))
    filtered_sent = []
    for w in tokenized_word:
        if (w not in stop_words) and (len(w) >= 3):
            filtered_sent.append(w)
    fdist = FreqDist(filtered_sent)

    fd = pd.DataFrame(fdist.most_common(16), columns=["Word", "Frequency"]).drop([0]).reindex()

    fig = go.Figure(data=[go.Pie(labels=list(fd['Word']),
                                 values=list(fd['Frequency']),
                                 hole=0.5,
                                 showlegend=False,
                                 hoverinfo='all',
                                 textinfo='label',
                                 automargin=False
                                 )],
                    layout={
                        'height': 260,
                            'width': 250,
                            'margin': {'l': 0,
                                       'r': 0,
                                       'b': 0,
                                       't': 0}})
    fig.update_layout(plot_bgcolor=colors['bgcolor'], paper_bgcolor=colors['bgcolor'],
                      annotations=[dict(visible=True,
                                        font_color='white',
                                        text=f'{fd["Word"].values[0].title()}',
                                        x=0.5,
                                        y=0.5,
                                        font_size=20,
                                        showarrow=False)])

    return fig



@app.callback(Output('table', 'data'),
              [Input('interval-component-slow', 'n_intervals')])
def sentimentable(n_intervals):

    # query for Table
    query = 'SELECT Created_at, Text, Polarity FROM twitter_table ORDER BY Created_at DESC'

    # Wrangling Table
    df_table = pd.read_sql_query(query, engine)
    df_table = df_table.head(10)
    df_table.loc[:, 'Polarity'] = df_table.loc[:, 'Polarity'].apply(lambda x: f'{x:.2f}')

    return df_table.to_dict('rows')

if __name__ == '__main__':
    app.run_server(debug=True, port='8800')

    # os.system('python3 data_collection.py')




