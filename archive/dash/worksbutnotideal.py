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
        dcc.Graph(id='live-graph', animate=True),
        dcc.Interval(
            id='graph-update',
            interval=1*1000,
        ),
    ]
)

@app.callback(Output('live-graph', 'figure'),
              [Input('graph-update', 'n_intervals')])
def update_graph(input_data):
    
    # [round_num, cost] = simulation(liquidity, rounds)
    # rounds.append(round_num)
    # costs.append(cost)
    
    [round_num, cost, probability] = simulation(liquidity, rounds)
    costs.append(cost)
    probabilities.append(probability)
    # round_l.append(round_num)
    
    df = pd.DataFrame({'cost': costs, 'probability': probabilities})

    data = plotly.graph_objs.Scatter(
            x=list(rounds),
            y=costs,
            # y=[df['cost'], df['probability']],
            name='Scatter',
            mode= 'lines+markers'
            )
    
    data2 = plotly.graph_objs.Scatter(
        x=list(rounds),
        y=probabilities,
        # y=[df['cost'], df['probability']],
        name='Scatter',
        mode= 'lines+markers'
        )

    return {'data': [data, data2], 'layout' : go.Layout(xaxis=dict(range=[min(rounds),max(rounds)]),
                                                yaxis=dict(range=[min(costs),max(costs)]),)}


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080 ,debug=True)