from settings import  colors, stop_words

# Data Wrangling for Pie Chart
import plotly.graph_objs as go

# Libraries working with data
import pandas as pd

# Libraries for Tokenization
import nltk
nltk.download('punkt')
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize

def pie_count(df):

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

    fig_2 = go.Figure(data=[go.Pie(labels=list(fd['Word']),
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
    fig_2.update_layout(
                        plot_bgcolor=colors['bgcolor'],
                        paper_bgcolor=colors['bgcolor'],
                        annotations=[dict(visible=True,
                                        font_color='white',
                                        text=f'{fd["Word"].values[0].title()}',
                                        x=0.5,
                                        y=0.5,
                                        font_size=20,
                                        showarrow=False)])

    return fig_2