import base64
import datetime
import io
import plotly.graph_objs as go
import cufflinks as cf

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table

import pandas as pd

import sqlite3
from components.agent import Agent
from components.params import MetaParams, Params
from doepy import build

from doe import doe

########################################################################################################################

# Static for single experiment but combinatorial runs - pass in params_tested, params_const, metaparams
params_tested = build.full_fact(
    {'liquidity': [100.0, 200.0],
     'num_rounds': [50.0, 100.0]}
)

# params_tested = build.full_fact(params_tested_input)

params_const = {
    'outcomes': ['A', 'B', 'C'],
    'agents_list': [Agent(1, 'first', 10000), Agent(2, 'second', 10000), Agent(3, 'third', 10000)],
    'mechanism': 'logarithmic',
    'i_shares': {'A': 0.0, 'B': 0.0, 'C': 0.0},
}
meta_params = MetaParams(
    params_tested=['liquidity', 'num_rounds'],
    params_const=['outcomes', 'agents_list', 'mechanism', 'i_shares'],
    results_primary=['cost', 'probability_A', 'probability_B',
                     'probability_C', 'shares_A', 'shares_B', 'shares_C'],
    results_full=['cost', 'probabilities', 'shares', 'p_shares', 'payments']
)

###############################################################################################################################

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

colors = {"graphBackground": "#F5F5F5",
          "background": "#ffffff", "text": "#000000"}

app.layout = html.Div(
    [
        html.Div(dcc.Input(id='experiment-name', value='placeholder', type='text')),

        html.Div(id='experiment-name-div', children='experiment_name'),
        dcc.Input(id='experiment-name-id',
                  value='experiment_name', type='text'),

        dcc.Upload(
            id="upload-data",
            children=html.Div(["Drag and Drop or ", html.A("Select Files")]),
            style={
                "width": "100%",
                "height": "60px",
                "lineHeight": "60px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
                "margin": "10px",
            },
            # Allow multiple files to be uploaded
            multiple=True,
        ),

        html.Div(dcc.Input(id='func-file', value='placeholder', type='text')),
        html.Div(dcc.Input(id='params-tested', value='placeholder', type='text')),
        html.Div(dcc.Input(id='params-const', value='placeholder', type='text')),
        html.Div(dcc.Input(id='results-primary', value='placeholder', type='text')),
        html.Div(dcc.Input(id='results-full', value='placeholder', type='text')),
        
        html.Button('Set Parameters', id='submit-val', n_clicks=0),
        html.Div(id='container-button-basic',
                 children='Enter a value and press submit'),

        html.Div(id='x-div', children='x_value'),
        dcc.Input(id='x-id', value='x_value', type='text'),

        html.Div(id='y-div', children='y_value'),
        dcc.Input(id='y-id', value='y_value', type='text'),

        dcc.Graph(id="Mygraph"),
        html.Div(id="output-data-upload"),
    ]
)


@app.callback(Output('Mygraph', 'figure'), [
    Input('upload-data', 'contents'),
    Input('upload-data', 'filename'),
    Input('x-id', 'value'),
    Input('y-id', 'value'),
])
def update_graph(contents, filename, x_value, y_value):
    x = []
    y = []
    if contents:
        contents = contents[0]
        filename = filename[0]
        df = parse_data(contents, filename)
        df = df.set_index(df.columns[0])
        x = df[x_value]
        y = df[y_value]
    fig = go.Figure(
        data=[
            go.Scatter(
                x=x,
                y=y,
                mode='markers')
        ],
        layout=go.Layout(
            plot_bgcolor=colors["graphBackground"],
            paper_bgcolor=colors["graphBackground"]
        ))
    return fig


def parse_data(contents, filename):
    content_type, content_string = contents.split(",")

    decoded = base64.b64decode(content_string)
    try:
        if "csv" in filename:
            # Assume that the user uploaded a CSV or TXT file
            df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
        elif "xls" in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
        elif "txt" or "tsv" in filename:
            # Assume that the user upl, delimiter = r'\s+'oaded an excel file
            df = pd.read_csv(io.StringIO(
                decoded.decode("utf-8")), delimiter=r"\s+")
    except Exception as e:
        print(e)
        return html.Div(["There was an error processing this file."])

    return df

# Inputs #####################################################################################################################


@app.callback(
    Output('container-button-basic', 'children'),
    [Input('submit-val', 'n_clicks')],
    [State('experiment-name', 'value'), State('func-file', 'value'), State('params-tested', 'value'), State('params-const', 'value'), State('results-primary', 'value'), State('results-full', 'value')]
)
def update_params(value, experiment_name, func_file, params_tested, params_const, results_primary, results_full):
    
    # params_tested = build.full_fact(
    # {'liquidity': [100.0, 200.0],
    #  'num_rounds': [50.0, 100.0]}
    # )

    # # params_tested = build.full_fact(params_tested_input)

    # params_const = {
    #     'outcomes': ['A', 'B', 'C'],
    #     'agents_list': [Agent(1, 'first', 10000), Agent(2, 'second', 10000), Agent(3, 'third', 10000)],
    #     'mechanism': 'logarithmic',
    #     'i_shares': {'A': 0.0, 'B': 0.0, 'C': 0.0},
    # }
    # meta_params = MetaParams(
    #     params_tested=['liquidity', 'num_rounds'],
    #     params_const=['outcomes', 'agents_list', 'mechanism', 'i_shares'],
    #     results_primary=['cost', 'probability_A', 'probability_B',
    #                     'probability_C', 'shares_A', 'shares_B', 'shares_C'],
    #     results_full=['cost', 'probabilities', 'shares', 'p_shares', 'payments']
    # )
    
    # run experiment
    doe(experiment_name, params_tested, params_const, meta_params, func_file)
    
    return '''The following parameters were updated:
            Experiment file: "{}" 
            Testing parameters: "{}" 
            Constant parmaeters: "{}" 
            Primary results: "{}" 
            Full results: "{}" 
            '''.format(value, func_file, params_tested, params_const, results_primary, results_full)


@app.callback(
    Output(component_id='experiment-name-div', component_property='children'),
    [Input(component_id='experiment-name-id', component_property='value')]
)
def update_div(input_value):
    experiment_name = input_value
    print("Updated experiment_name", experiment_name)
    return 'Experiment Name: "{}"'.format(input_value)


@app.callback(
    Output(component_id='x-div', component_property='children'),
    [Input(component_id='x-id', component_property='value')]
)
def update_div(input_value):
    x_value = input_value
    print("Updated x_value: ", x_value)
    return 'X value: "{}"'.format(input_value)


@app.callback(
    Output(component_id='y-div', component_property='children'),
    [Input(component_id='y-id', component_property='value')]
)
def update_div(input_value):
    y_value = input_value
    print("Updated y_value: ", y_value)
    return 'Y value: "{}"'.format(input_value)

###############################################################################################################################


@app.callback(
    Output("output-data-upload", "children"),
    [Input("upload-data", "contents"), Input("upload-data", "filename")],
)
def update_table(contents, filename):
    table = html.Div()

    if contents:
        contents = contents[0]
        filename = filename[0]
        df = parse_data(contents, filename)

        table = html.Div(
            [
                html.H5(filename),
                dash_table.DataTable(
                    data=df.to_dict("rows"),
                    columns=[{"name": i, "id": i} for i in df.columns],
                ),
                html.Hr(),
                html.Div("Raw Content"),
                html.Pre(
                    contents[0:200] + "...",
                    style={"whiteSpace": "pre-wrap", "wordBreak": "break-all"},
                ),
            ]
        )

    return table


if __name__ == "__main__":
    app.run_server(debug=True)

