import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# The global app object
app = dash.Dash(__name__)

# The layout, including html, widgets and figures
app.layout = html.Div(children=[
    html.H1(children='Hello'),
    html.Div(id='my-div', children='Your text will go here!'),
    dcc.Input(id='my-id', value='initial value', type='text'),
    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'A'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': 'B'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )
])

# A callback example
@app.callback(
    Output(component_id='my-div', component_property='children'),
    [Input(component_id='my-id', component_property='value')]
)
def update_div(input_value):
    return 'You entered "{}"'.format(input_value)

if __name__ == '__main__':
    app.run_server(debug=True)
    
    
    
@app.callback(Output('Mygraph', 'figure'), [
Input('upload-data', 'contents'),
Input('upload-data', 'filename')
])
def update_graph(contents, filename):
    x = []
    y = []
    if contents:
        contents = contents[0]
        filename = filename[0]
        df = parse_data(contents, filename)
        df = df.set_index(df.columns[0])
        x=df['DATE']
        y=df['TMAX']
    fig = go.Figure(
        data=[
            go.Scatter(
                x=x, 
                y=y, 
                mode='lines+markers')
            ],
        layout=go.Layout(
            plot_bgcolor=colors["graphBackground"],
            paper_bgcolor=colors["graphBackground"]
        ))
    return fig