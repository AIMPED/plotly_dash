from dash import Dash, dcc, html, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
from scipy.ndimage import rotate
import plotly.express as px
from PIL import Image
import urllib.request
import numpy as np
import math


# get an example image from url
urllib.request.urlretrieve(
    'https://raw.githubusercontent.com/michaelbabyn/plot_data/master/bridge.jpg',
    'bridge.jpg'
)

# open image and create plotly figure, locally stored images can be used this way too
img = Image.open('bridge.jpg')
img_arr = np.array(img)
fig = px.imshow(img=img)

# update figure layout
fig.update_layout(
    dragmode='zoom',
    template='plotly_dark',
    plot_bgcolor='rgba(0, 0, 0, 0)',
    paper_bgcolor='rgba(0, 0, 0, 0)',
    width=img.width * 0.45,
    height=img.height * 0.45,
    margin={
        'l': 0,
        'r': 0,
        't': 20,
        'b':0,
        },
    xaxis={
        'showgrid': False,
        'showticklabels': False
        },
    yaxis={
        'showgrid': False,
        'showticklabels': False
        },
    # style for the annotations
    newshape={
        'fillcolor': 'rgba(1.0, 1.0, 1.0, 0.2)',
        'opacity': 1.0,
        'line':{
            'color': '#E2F714',
            'width': 2,
            }
        }
)

# add config for annotations
config = {
    'scrollZoom': True,
    'displayModeBar': True,
    'modeBarButtonsToAdd': [
        'drawline',
        'drawrect',
        'eraseshape',
    ],
    'modeBarButtonsToRemove': [
        'zoom2d',
        'pan2d',
        'zoomin2d',
        'zoomout2d',
        'autoScale2d',
        'resetScale2d',
        'toimage'
    ],
    'displaylogo': False
}

# app initialization
app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE],
           meta_tags=[{'name': 'viewport',
                       'content': 'width=device-width, initial-scale=1.0'}]
           )

# app layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id='org_img',
                figure=fig,
                config=config
            ),
            dcc.Graph(
                id='chgd_img',
                figure=fig,
                config={'displayModeBar': False}
            )
        ], width={'size': 5, 'offset': 0}
        ),
        dbc.Col([
            dcc.Markdown('''
                ## Rotation
                - draw a line (modebar button) on the  **upper image**
                - choose the alignemnt mode (vertiacal/ horizontal)
                - check "invert rotation" if necessary
                - click "rotate" button
                '''),
            html.Button(
                'rotate',
                id='rotate',
                n_clicks=None,
            ),
            dbc.Checklist(
                id='invert',
                options=[{'label': 'invert rotation', 'value': True}]
            ),
            dcc.RadioItems(
                id='alignment',
                options=['horizontal', 'vertical'],
                value='horizontal',
                inline=True,
                inputStyle={"margin-right": "5px"},
                labelStyle={"margin-right": "10px"}
            ),
            html.Br(),
            dcc.Markdown('''
                ## Crop
                - draw rectangle (modebar button)  on the  **upper image**
                - click "crop" button
                '''),           
            html.Button(
                'crop',
                id='crop',
                n_clicks=None
            ),
        ], width={'size': 5, 'offset': 0}
        ),
        dbc.Col(
            html.A(
                html.Button('Refresh Page'),
                href='/'
                ),
            width={'size': 1, 'offset': 0}
        )
    ], justify='around'
    ),
], fluid=True
)


# callback for annotations
@app.callback(
    Output('chgd_img', 'figure'),
    State('org_img', 'figure'),
    State('alignment', 'value'),
    State('invert', 'value'),
    Input('rotate', 'n_clicks'),
    Input('crop', 'n_clicks'),
    prevent_initial_call=True,
)
def rotate_crop(org_img, alignment, invert, rotate_click, crop_click):
    # trigger which button has been clicked
    trigger_id = callback_context.triggered[0]['prop_id']
    
    # get figure layout
    layout = org_img.get('layout', {})
    
    # get annotations
    annotations = layout.get('shapes', {})
    
    # set default figure
    figure = org_img

    if trigger_id == 'rotate.n_clicks':
        for shape in annotations:
            t = shape.get('type', '')
            if t == 'line':
                # get coordinates of points
                p0 = np.array([shape.get(c) for c in ['x0', 'y0']])
                p1 = np.array([shape.get(c) for c in ['x1', 'y1']])

                # calculate delta
                d = abs(p1 - p0)

                # control alignment h/v
                if alignment == 'horizontal':
                    d = np.flip(d)
                    angle = math.degrees(np.arctan2(*d))
                else:
                    angle = -math.degrees(np.arctan2(*d))

                # necessary due to selection order of p0, p1
                if invert:
                    angle = -angle

                # rotate image and create plotly figure
                rotated = rotate(img, angle)
                figure = px.imshow(rotated)
                break
    else:
        for shape in annotations:
            t = shape.get('type', '')
            if t == 'rect':
                x = [int(shape.get(c)) for c in ['x0', 'x1']]
                y = [int(shape.get(c)) for c in ['y0', 'y1']]
                figure = px.imshow(img_arr[min(y):max(y), min(x):max(x),:])
                break

    # update figure layout
    figure.update_layout(
                    dragmode='zoom',
                    template='plotly_dark',
                    plot_bgcolor='rgba(0, 0, 0, 0)',
                    paper_bgcolor='rgba(0, 0, 0, 0)',
                    margin={
                        'l': 0,
                        'r': 0,
                        't': 20,
                        'b':0,
                        },
                    xaxis={
                        'showgrid': False,
                        'showticklabels': False
                        },
                    yaxis={
                        'showgrid': False,
                        'showticklabels': False
                        }
                )
    return figure


if __name__ == '__main__':
    app.run_server(debug=True, port=8051)
