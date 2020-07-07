@app.callback(Output('table', 'data'),
              [Input('interval-component-slow', 'n_intervals')])
def sentimentable(n_intervals):

    # query for Table
    query = 'SELECT Created_at, Text, Polarity FROM twitter_table ORDER BY Created_at DESC'

    # Wrangling Table
    df_table = pd.read_sql_query(query, engine)
    df_table.loc[:, 'Created_at'] = pd.to_datetime(df_table['Created_at']).apply(lambda x: x + timedelta(hours=6))
    df_table = df_table.head(10)
    df_table.loc[:, 'Polarity'] = df_table.loc[:, 'Polarity'].apply(lambda x: f'{x:.2f}')

    return df_table.to_dict('rows')