import plotly.graph_objs as go
from settings import colors

def pie_sent(df):
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