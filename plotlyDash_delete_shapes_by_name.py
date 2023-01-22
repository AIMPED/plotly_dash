from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
import numpy as np

# prepare trace data
data = go.Scatter(
    x=[1, 10],
    y=[1, 10],
    mode='markers',
    marker={
        'size': 8,
        'symbol': 'circle-open',
    },
)

# create figure
fig = go.Figure(data=data)

# update layout
fig.update_layout(
    template='plotly_dark',
    plot_bgcolor='rgba(0, 0, 0, 0)',
    paper_bgcolor='rgba(0, 0, 0, 0)',
    width=700,
    height=500,
    margin={
        'l': 0,
        'r': 0,
        't': 20,
        'b': 100,
    }
)

# add some shapes
for i in range(1, 6):
    fig.add_shape(
        {
            'type': 'rect',
            'x0': np.random.randint(1, 5), 'x1': np.random.randint(6, 11),
            'y0': np.random.randint(1, 5), 'y1': np.random.randint(6, 11),
        },
        editable=True,
        name=f'shape_{i}',
        line={
            'color': ['red', 'yellow', 'blue', 'pink'][np.random.randint(0, 4)],
            'width': 2,
            'dash': 'solid'
        },
    )

# Build App
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.SLATE],
    meta_tags=[
        {
            'name': 'viewport',
            'content': 'width=device-width, initial-scale=1.0'
        }
    ]
)

# app layout
app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                dcc.Graph(
                    id='graph',
                    figure=fig,
                    config={
                        'scrollZoom': True,
                        'displayModeBar': False,
                    }
                ),
                width={'size': 5, 'offset': 0}
            ), justify='around'
        ),
        dbc.Row(
            [
                dbc.Col(html.H5('Click button to delete shapes')),
                dbc.Col(html.H5('Enter name of shape to delete')),
                dbc.Col(html.H5('Available shapes'))
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.Button(
                        'Delete',
                        id='delete'
                    ),
                ),
                dbc.Col(
                    dcc.Input(
                        id='box',
                        type='text',
                        value='shape_x',
                        className='input'
                    ),
                ),
                dbc.Col(
                    html.Div(
                        id='available',
                        children=', '.join([f'shape_{i}' for i in range(1, 6)])
                    )
                ),
            ], justify='around'
        )
    ], fluid=True
)


@app.callback(
    Output('graph', 'figure'),
    Output('available', 'children'),
    Input('delete', 'n_clicks'),
    State('graph', 'figure'),
    State('box', 'value'),
)
def get_click(click, current_figure, shape_to_delete):
    if not click:
        raise PreventUpdate
    else:
        # get existing shapes
        shapes = current_figure['layout'].get('shapes')

        # delete shape, aka keep only the shapes which are not to be deleted
        shapes[:] = [shape for shape in shapes if shape.get('name') != shape_to_delete]

        # update figure layout
        current_figure['layout'].update(shapes=shapes)
    return current_figure, ', '.join([shape.get('name') for shape in shapes])


if __name__ == '__main__':
    app.run(debug=True, port=8053)

