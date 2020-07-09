from datetime import timedelta
import pandas as pd

def twit_table(query, engine):
    # Wrangling Table
    df_table = pd.read_sql_query(query, engine)
    df_table.loc[:, 'Added_at'] = pd.to_datetime(df_table['Added_at']).apply(lambda x: x + timedelta(hours=6))
    df_table['Added_at'] = df_table['Added_at'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
    df_table = df_table.head(10)
    df_table.loc[:, 'Polarity'] = df_table.loc[:, 'Polarity'].apply(lambda x: f'{x:.2f}')

    return df_table.to_dict('rows')