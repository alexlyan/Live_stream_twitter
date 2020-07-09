from settings import colors

# Scatter Figure
import plotly.graph_objs as go

# Libraries working with data
import pandas as pd
from datetime import datetime
from datetime import timedelta


def scatter_plot(df):
    df.loc[:, 'Added_at'] = pd.to_datetime(df['Added_at']).apply(lambda x: x + timedelta(hours=6))
    df = df[df['Added_at'] >= (datetime.now() - timedelta(minutes=30))]
    result = df.groupby([pd.Grouper(freq='10s', key='Added_at'), 'Polarity']).count().unstack(
        fill_value=0).stack().reset_index()
    timeseries = result['Added_at'][result['Polarity'] == 0].reset_index(drop=True)

    scatter = go.Figure(
        layout={'width': 1000,
                'legend': {'font': {'color': 'white',
                                    'size': 8}},

                }
    )
    # Create the graph
    scatter.add_trace(go.Scatter(
        x=timeseries,
        y=result['Text'][result['Polarity'] == 0],
        name="Neutrals",
        showlegend=True,
        opacity=0.8,
        mode='lines',
        line=dict(width=0.5,
                  color='#0080ff'),
        stackgroup='one'
    ))
    scatter.add_trace(go.Scatter(
        x=timeseries,
        y=result['Text'][result['Polarity'] > 0.4],
        name="Positive",
        opacity=0.8,
        line=dict(width=0.5,
                  color='#725EB7'),
        mode='lines',
        stackgroup='two'
    ))
    scatter.add_trace(go.Scatter(
        x=timeseries,
        y=result['Text'][result['Polarity'] <= -0.4],
        name="Negative",
        opacity=0.8,
        line=dict(width=0.5,
                  color='#FF6792'),
        mode='lines',
        stackgroup='three'
    ))

    scatter.update_layout(plot_bgcolor=colors['bgcolor'],
                          paper_bgcolor=colors['bgcolor'],
                          xaxis=dict(visible=True,
                                     color='white')
                          )

    return scatter
