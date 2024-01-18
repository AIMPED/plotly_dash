from dash import Dash, html, dcc, Input, Output
import plotly.graph_objects as go
import numpy as np
import json


# load some data
pts = np.loadtxt(
    np.DataSource().open('https://raw.githubusercontent.com/plotly/datasets/master/mesh_dataset.txt')
)

# transpose arrays
x, y, z = pts.T

# create base figure
fig = go.Figure(
    go.Mesh3d(
        x=x,
        y=y,
        z=z,
        color='lightpink',
        opacity=0.50,
        hoverinfo='skip'
    )
)

# add scatter trace
fig.add_scatter3d(
    x=[1, 2, 3],
    y=[1, 2, 3],
    z=[1, 2, 3],
    mode='markers+lines',
)

app = Dash(
    __name__,
    external_stylesheets=[
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css",
    ]
)

app.layout = html.Div(
    [
        html.Div(
            className='col-4',
            children=dcc.Graph(id='graph', figure=fig)
        ),
        html.Div(
            id='out_0',
            className='col-2'
        ),
        html.Div(
            id='out_1',
            className='col-2'
        ),
        html.Div(
            id='out_2',
            className='col-2'
        ),
        html.Div(
            id='out_3',
            className='col-2'
        ),
    ],
    className='row'
)


@app.callback(
    Output('out_0', 'children'),
    Output('out_1', 'children'),
    Output('out_2', 'children'),
    Output('out_3', 'children'),
    Input('graph', 'clickData'),
    Input('graph', 'hoverData'),
    Input('graph', 'relayoutData'),
    Input('graph', 'restyleData'),
    prevent_initial_call=True
)
def update(click_data, hover_data, relayout_data, restyle_data):
    return [
        html.Pre([html.H5('click data'), json.dumps(click_data, indent=3)]),
        html.Pre([html.H5('hover data'), json.dumps(hover_data, indent=3)]),
        html.Pre([html.H5('relayout data'), json.dumps(relayout_data, indent=3)]),
        html.Pre([html.H5('restyle data'), json.dumps(restyle_data, indent=3)])
    ]


if __name__ == "__main__":
    app.run_server(debug=True)
