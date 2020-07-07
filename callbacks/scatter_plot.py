# Scatter Figure

    # Convert UTC into PDT
    df.loc[:, 'Created_at'] = pd.to_datetime(df['Created_at']).apply(lambda x: x + timedelta(hours=6))
    df = df[df['Created_at'] >= (datetime.now() - timedelta(minutes=30))]
    result = df.groupby([pd.Grouper(freq='10s', key='Created_at'), 'Polarity']).count().unstack(
        fill_value=0).stack().reset_index()

    scatter = go.Figure(
        layout={'width': 1000,
            'legend': {'font': {'color': 'white',
                                    'size': 8}},

        }
    )
    # Create the graph
    scatter.add_trace(go.Scatter(
        x=result['Created_at'][result['Polarity'] == 0],
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
        x=result['Created_at'][result['Polarity'] > 0.4],
        y=result['Text'][result['Polarity'] > 0.4],
        name="Positive",
        opacity=0.8,
        line=dict(width=0.5,
                  color='#725EB7'),
        mode='lines',
        stackgroup='two'
    ))
    scatter.add_trace(go.Scatter(
        x=result['Created_at'][result['Polarity'] <= -0.4],
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