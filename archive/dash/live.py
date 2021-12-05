import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
import plotly.graph_objs as go
from collections import defaultdict
import pandas as pd

from prediction import *

rounds = list(range(100)) # [1, 2, 3, ..., 100]
costs = []
probabilities = []
liquidity = 100


app = dash.Dash(__name__)
app.layout = html.Div(
    [
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
        
        # html.Div(id='rounds_slctd_txt', children=[]),
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

        # html.Div(id='liquidity_slctd_txt', children=[]),
        html.Br(),
    
        dcc.Graph(id='live-graph', animate=True),
        # dcc.Interval(
        #     id='graph-update',
        #     interval=1*1000,
        # ),
        
    ]
)

@app.callback([Output('live-graph', 'figure'),
        Output(component_id='liquidity_slctd_txt', component_property='children'),
        Output(component_id='rounds_slctd_txt', component_property='children')],
        [Input(component_id='slct_liquidity', component_property='value'),
        Input(component_id='slct_rounds', component_property='value')])
def update_graph(liquidity_slctd, rounds_slctd):
    
    # [round_num, cost] = simulation(liquidity, rounds)
    # rounds.append(round_num)
    # costs.append(cost)
    
    [round_num, cost, probability] = simulation(liquidity_slctd, rounds_slctd)
    costs.append(cost)
    probabilities.append(probability)
    # round_l.append(round_num)
    
    df = pd.DataFrame({'cost': costs, 'probability': probabilities})

    d_costs = plotly.graph_objs.Scatter(
            x=list(rounds),
            y=costs,
            # y=[df['cost'], df['probability']],
            name='Scatter',
            mode= 'lines+markers'
            )
    
    d_probabilities = plotly.graph_objs.Scatter(
        x=list(rounds),
        y=probabilities,
        # y=[df['cost'], df['probability']],
        name='Scatter',
        mode= 'lines+markers'
        )

    # liquidity_slctd_txt = "The liquidity chosen by user was: {}".format(liquidity_slctd)
    # rounds_slctd_txt = "The rounds chosen by user was: {}".format(rounds_slctd)

    return {'data': [d_costs, d_probabilities], 'layout' : go.Layout(xaxis=dict(range=[min(rounds),max(rounds)]),
                    yaxis=dict(range=[min(costs),max(costs)]))}
    #, liquidity_slctd_txt, rounds_slctd_txt


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080 ,debug=True)