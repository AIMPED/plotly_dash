from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import plotly.express as px
import numpy as np

# create image and plotly express object
img = np.random.randint(0, 255, (90, 160))
fig = px.imshow(img, color_continuous_scale='Blugrn')

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
        'b': 0,
    }
)

# hide color bar
fig.update_coloraxes(showscale=False)

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
                dbc.Col(
                    [
                        html.A(
                            html.Button(
                                'Refresh Page',
                                id='refresh_button'
                            ),
                            href='/'
                        ),
                        dcc.Markdown(
                            '''
                            # Functionality:
                            - click anywhere on the image, shape is created at click position
                            - use the "Refresh Page" button to reload the image
                            '''
                        ) 
                    ], width={'size': 5, 'offset': 0}
                ),
            ], justify='around'
        )
    ], fluid=True
)


@ app.callback(
    Output('graph', 'figure'),
    State('graph', 'figure'),
    Input('graph', 'clickData')
)
def get_click(graph_figure, clickData):
    if not clickData:
        raise PreventUpdate
    else:
        points = clickData.get('points')[0]
        x = points.get('x')
        y = points.get('y')

        # create new shape
        new_shape = create_shape(x=x, y=y, size=5)

        # get existing shapes
        shapes = graph_figure['layout'].get('shapes')
        if not shapes:
            shapes = []
        shapes.extend(new_shape)

        # update figure layout
        graph_figure['layout'].update(shapes=shapes)
    return graph_figure


def create_shape(x, y, size=4, color='rgba(39,43,48,255)'):
    """
    function creates a shape for a dcc.Graph object

    Args:
        x: x coordinate of center point for the shape
        y: y coordinate of center point for the shape
        size: size of annotation (diameter)
        color: (rgba / rgb / hex) string or any other color string recognized by plotly

    Returns:
        a list containing a dictionary, keys corresponding to dcc.Graph layout update
    """
    shape = [
        {
            'editable': True,
            'xref': 'x',
            'yref': 'y',
            'layer': 'above',
            'opacity': 1,
            'line': {
                'color': color,
                'width': 1,
                'dash': 'solid'
            },
            'fillcolor': color,
            'fillrule': 'evenodd',
            'type': 'circle',
            'x0': x - size / 2,
            'y0': y - size / 2,
            'x1': x + size / 2,
            'y1': y + size / 2
        }
    ]
    return shape


if __name__ == '__main__':
    app.run_server(debug=True, port=8053)
