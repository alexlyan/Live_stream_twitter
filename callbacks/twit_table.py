# def quick_color(s):
#     # except return bg as app_colors['background']
#     if s >= 0.3:
#         # positive
#         return "#002C0D"
#     elif s <= -0.3:
#         # negative:
#         return "#270000"
#
#     else:
#         return '#173F5F'
#
#
# def generate_table(df, max_rows=5):
#     return html.Table(className="responsive-table",
#                       children=[
#                           html.Thead(
#                               html.Tr(
#                                   children=[
#                                       html.Th(col.title()) for col in df.columns.values],
#                                   style={'color': '#e7eff6',
#                                          'font-size': 10,
#                                          'size': 2}
#                               )
#                           ),
#                           html.Tbody(
#                               [
#
#                                   html.Tr(
#                                       children=[
#                                           html.Td(data) for data in d
#                                       ], style={'color': '#e7eff6',
#                                                 'background-color': quick_color(d[2]),
#                                                 'font-size': 10,
#                                                 'size': 2}
#                                   )
#                                   for d in df.values.tolist()])
#                       ]
#                       )