# LIVE EXPERIMENTATION
# DASH UI

import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)
from .simulation.doe import doe


app = Dash(__name__)

df = pd.read_csv('bees.csv')

df = df.groupby(['State', 'ANSI', 'Affected by', 'Year', 'state_code'])[['Pct of Colonies Impacted']].mean()
df.reset_index(inplace=True)
print(df[:5])

# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H1("Dashboard", style={'text-align': 'center'}),
    
    dcc.Dropdown(id="slct_liquidity",
                 options=[
                     {"label": "100", "value": 100},
                     {"label": "200", "value": 200},
                     {"label": "300", "value": 300},
                     {"label": "400", "value": 400}],
                 multi=False,
                 value=100, # default value
                 style={'width': "40%"}
                 ),
    
    html.Div(id='rounds_slctd_txt', children=[]),
    html.Br(),  
    
    dcc.Dropdown(id="slct_rounds",
                 options=[
                     {"label": "100", "value": 100},
                     {"label": "500", "value": 500},
                     {"label": "1000", "value": 1000},
                     {"label": "5000", "value": 5000}],

                 multi=False,
                 value=100, # default value
                 style={'width': "40%"}
                 ),

    html.Div(id='liquidity_slctd_txt', children=[]),
    html.Br(),

    dcc.Graph(id='my_bee_map', figure={})

])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='liquidity_slctd_txt', component_property='children'),
     Output(component_id='rounds_slctd_txt', component_property='children'), 
     Output(component_id='my_bee_map', component_property='figure')],
    [Input(component_id='slct_liquidity', component_property='value'),
     Input(component_id='slct_rounds', component_property='value')]
)
def update_graph(liquidity_slctd, rounds_slctd):
    print(liquidity_slctd)
    print(type(liquidity_slctd))
    print(rounds_slctd)
    print(type(rounds_slctd))

    liquidity_slctd_txt = "The liquidity chosen by user was: {}".format(liquidity_slctd)
    rounds_slctd_txt = "The rounds chosen by user was: {}".format(rounds_slctd)

    # always copy the dataframe to avoid changes to the original dataframe
    dff = df.copy()
    dff = dff[dff["Year"] == liquidity_slctd]
    dff = dff[dff["Affected by"] == "Varroa_mites"]
    # print(dff)

    # Plotly Express
    fig = px.choropleth(
        data_frame=dff,
        locationmode='USA-states',
        locations='state_code',
        scope="usa",
        color='Pct of Colonies Impacted',
        hover_data=['State', 'Pct of Colonies Impacted'],
        color_continuous_scale=px.colors.sequential.YlOrRd,
        labels={'Pct of Colonies Impacted': '% of Bee Colonies'},
        template='plotly_dark'
    )

    # Plotly Graph Objects (GO)
    # fig = go.Figure(
    #     data=[go.Choropleth(
    #         locationmode='USA-states',
    #         locations=dff['state_code'],
    #         z=dff["Pct of Colonies Impacted"].astype(float),
    #         colorscale='Reds',
    #     )]
    # )
    #
    # fig.update_layout(
    #     title_text="Bees Affected by Mites in the USA",
    #     title_xanchor="center",
    #     title_font=dict(size=24),
    #     title_x=0.5,
    #     geo=dict(scope='usa'),
    # )

    return liquidity_slctd_txt, rounds_slctd_txt, fig


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)