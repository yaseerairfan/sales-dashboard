# ---------------------------------Load libraries-------------------------------------
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# ---------------------------------Load data-------------------------------------


data = pd.read_csv('data/SampleSuperstore(task2).csv')

def get_options(ddlist):
    dict_list = []
    for i in ddlist:
        dict_list.append({'label': i, 'value': i})

    return dict_list


y = data.groupby(['Category', 'Region'], as_index=False).sum()
print(y)
# ---------------------------------Initialise the app-------------------------
app = dash.Dash(__name__)

# ---------------------------------Define the app-------------------------------
card_content1 = [
    dbc.CardBody(
        [
            html.H5("TOTAL SALES", className="card-title", style={'marginTop': '11px', 'marginBottom': '36px'}),
            html.P(id='card1',
                   className="card-text"
                   ),
        ]
    ),
]
card_content2 = [
    dbc.CardBody(
        [
            html.H5("TOTAL PROFIT", className="card-title", style={'marginTop': '11px', 'marginBottom': '36px'}),
            html.P(
                id='card2',
                className="card-text"
            ),
        ]
    ),
]
app.layout = html.Div(children=[
    html.Div(className='row main_div',  # Define the row element
             children=[
                 html.Div(className='four columns div-user-controls',
                          children=[
                              html.H2('SUPER STORE SALES DASHBOARD',
                                      style={'text-align-last': 'end', 'margin-top': '-52px'}),
                              html.P('''Visualising sales data with Plotly - Dash'''),
                              html.P('''Pick one or more item from the dropdown below.'''),

                              html.Div(
                                  [
                                      dbc.Row(
                                          [
                                              dbc.Col(dbc.Card(card_content1, color="primary", inverse=True)),

                                              dbc.Col(dbc.Card(card_content2, color="info", inverse=True)),
                                          ],
                                          className="mb-6",
                                          style={'display': 'flex', 'marginTop': '23px'}
                                      )

                                  ]
                              ),
                              html.Div(className='pie_chart', children=[

                                  dcc.Graph(id='piechart'),
                                  html.H4('TOTAL QUANTITY', style={'margin-bottom': '10px','margin-top':'-10px'})
                              ])
                          ]),

                 # Define the left element
                 html.Div(className='eight columns div-for-charts bg-grey',
                          children=[
                              html.H1(id='bhead', style={'textAlign': 'center'}),
                              html.Div(className='div-for-dropdown',
                                       children=[
                                           html.Div(className='dd1',
                                                    children=[
                                                        dcc.Dropdown(
                                                             id='stockselector1',
                                                             options=get_options(data['City'].unique()),
                                                             multi=False,
                                                             value=data['City'].sort_values()[0],
                                                             style={'backgroundColor': '#1E1E1E'},
                                                             className='stockselector'
                                                                    )
                                                                ],
                                                    style={'width': '30%', 'paddingRight': '10px'}
                                                    ),

                                           html.Div(className='dd2',
                                                    children=[
                                                        dcc.Dropdown(
                                                            id='stockselector2',
                                                            options=get_options(data['Ship Mode'].unique()),
                                                            multi=False,
                                                            value=data['Ship Mode'].sort_values()[0],
                                                            style={'backgroundColor': '#1E1E1E'},
                                                            className='stockselector'),
                                                              ],
                                                    style={'width': '30%','paddingRight': '10px'}
                                                    ),
                                           html.Div(className='dd3',
                                                    children=[
                                                        dcc.Dropdown(
                                                            id='stockselector3',
                                                            options=get_options(data['Segment'].unique()),
                                                            multi=False,
                                                            value=data['Segment'].sort_values()[0],
                                                            style={'backgroundColor': '#1E1E1E'},
                                                            className='stockselector'
                                                                    )

                                                            ],
                                                    style={'width': '30%'}
                                                    )
                                       ]),

                              dcc.Graph(id='barchart'),
                              html.Br(),
                              html.H1('REGION WISE PURCHASE', style={'textAlign': 'center'}),
                              dcc.Graph(id='timeseries',
                                        config={'displayModeBar': False},
                                        animate=True,
                                        figure=px.line(y,
                                                       x='Category',
                                                       y='Quantity',
                                                       color='Region',
                                                       template='plotly_dark')
                                        .update_layout(
                                            {'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                                             'paper_bgcolor': 'rgba(0, 0, 0, 0)'
                                             })
                                        )

                          ]),  # Define the right element

             ])

])


# ---connecting graphs with dash components----


@app.callback(
    [Output('bhead', 'children'),
     Output('barchart', 'figure'),
     Output('card1', 'children'),
     Output('card2', 'children'),
     Output('piechart', 'figure')],
    [Input('stockselector1', 'value'),
     Input('stockselector2', 'value'),
     Input('stockselector3', 'value')]
)
def updatechart(City, ShipMode, Segment):
    heading = 'SALES AND PROFIT IN {}'.format(str.upper(City))
    d = data.loc[(data['City'] == City) & (data['Ship Mode'] == ShipMode) & (data['Segment'] == Segment)]
    dff = d.groupby('Sub-Category', as_index=False).sum()
    totalsale = int(dff['Sales'].sum())
    totalprofit = int(dff['Profit'].sum())
    bar = px.bar(dff, x='Sub-Category', y='Sales',
                 hover_data=['Profit', 'Quantity'], color='Profit',
                 labels={'sale': 'Sales in {}'.format(City)},
                 template='plotly_dark',
                 height=400
                 ).update_layout(
        {'plot_bgcolor': 'rgba(0, 0, 0, 0)',
         'paper_bgcolor': 'rgba(0, 0, 0, 0)'
         })
    pie = px.pie(dff, values='Quantity', names='Sub-Category', color_discrete_sequence=px.colors.sequential.RdBu,
                 template='plotly_dark').update_layout(
        {'plot_bgcolor': '#1E1E1E',
         'paper_bgcolor': '#1E1E1E'
         })
    return heading, bar, totalsale, totalprofit, pie


# --------------------------------- Run the app---------------------------------

if __name__ == '__main__':
    app.run_server(debug=True)
