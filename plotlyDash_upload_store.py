from dash import Dash, dcc, html, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
from base64 import b64decode
import plotly.express as px
import urllib.request
from PIL import Image
import numpy as np
import json

# get an example image from url
urllib.request.urlretrieve(
    'https://raw.githubusercontent.com/michaelbabyn/plot_data/master/bridge.jpg',
    'bridge.jpg'
)

# open image and create plotly figure
img = Image.open('bridge.jpg')
fig = px.imshow(img=img)

# create layout for figure
layout = {
    'dragmode': 'drawrect',
    'template': 'plotly_dark',
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    'width': img.width * 0.45,
    'height': img.height * 0.45,
    'margin': {
        'l': 0,
        'r': 0,
        't': 20,
        'b': 0,
    },
    'xaxis': {
        'showgrid': False,
        'showticklabels': False
    },
    'yaxis': {
        'showgrid': False,
        'showticklabels': False
    },
    # style for the annotations
    'newshape': {
        'fillcolor': 'rgba(1.0, 1.0, 1.0, 0.2)',
        'opacity': 1.0,
        'line': {
            'color': '#E2F714',
            'width': 2,
        }
    },
}

# update figure layout
fig.update_layout(layout)

# config for dcc.Graph
# add/remove annotations buttons, make mode bar visible all time
config = {
    'scrollZoom': True,
    'displayModeBar': True,
    'modeBarButtonsToAdd': [
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
    'displaylogo': False,
}


# utility function
def parse_file(content):
    """
    function parses a Base64 text

    Args:
         content: base64 text
    Returns:
        annotations: dictionary
    """
    # split text with ',', first par of string contains information concerning type
    _, base64_text = content.split(',')

    # convert to byte string
    byte_string = b64decode(base64_text)

    # convert to utf-8 string
    utf_string = byte_string.decode('utf-8')

    # converting "true" to uppercase so that it gets evaluated as True
    utf_string = utf_string.replace('true', 'True')

    # convert string dictionary into dictionary
    annotations = eval(utf_string)
    return annotations


# app initialization
app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE],
           meta_tags=[{'name': 'viewport',
                       'content': 'width=device-width, initial-scale=1.0'}]
           )

# app layout
app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                        id='graph',
                        figure=fig,
                        config=config
                    ),
                    width={'size': 4, 'offset': 0}
                ),
                dbc.Col(
                    id='post',
                    children=[],
                    width={'size': 4, 'offset': 0}
                ),
                dbc.Col(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        dbc.Button(
                                            'Save into dcc.Store',
                                            id='save_ann',
                                            n_clicks=None,
                                            style={'width': '50%'}
                                        ),
                                        dbc.Button(
                                            'Delete dcc.Store',
                                            id='delete',
                                            n_clicks=None,
                                            style={'width': '50%'}
                                        ),
                                    ], className="d-flex flex-row"
                                ),
                                html.Div(
                                    [
                                        dbc.Button(
                                            'Export to file',
                                            id='export',
                                            n_clicks=None,
                                            style={'width': '50%'}
                                        ),
                                        dcc.Upload(
                                            id='upload-data',
                                            # accept only text files
                                            accept='.txt',
                                            # Do not allow multiple files to be uploaded
                                            multiple=False,
                                            children=dbc.Button(
                                                'Import from file',
                                                style={'width': '100%'}
                                            ),
                                            style={'width': '100%'}
                                        )
                                    ], className="d-flex flex-row"
                                ),
                                dbc.Button(
                                    'Copy annotations to other figure',
                                    id='ret_ann',
                                    n_clicks=None,
                                    style={'width': '100%'}
                                ),
                            ]
                        )
                    ], width={'size': 2, 'offset': 0}
                )
            ], justify='around'
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H4('dcc.Store content'),
                        html.Pre(id='store_in')
                    ], width={'size': 5, 'offset': 1}
                ),
                dbc.Col(
                    dcc.Markdown(
                        '''
                    #### Functionality:
                    - draw/delete annotation(s) on the image
                    - "Save into dcc.Store": saves annotations in store
                    - "Export to file": saves the annotations into a text file
                    - "Delete dcc.Store": deletes all contents form dcc.Store
                    - "Copy annotations to other figure": copys the data in dcc.Store to an image

                    The content of the dcc.Store element is always displayed
                    '''),
                    width={'size': '5'}
                ),
                dbc.Col(
                    [
                        dcc.Store(
                            id='store',
                            data={},
                            storage_type='memory'
                        ),
                        html.Pre(
                            id='dummy_out',
                            style={'display': 'none'}
                        )
                    ]
                ),
            ], justify='around'
        )
    ], fluid=True
)


# callback for button functionality
# click on "delete" button: empty dcc.Store
# click on "save" button: get annotations from figure, write into dcc.Store
# click on upload: load annotations from text file
@ app.callback(
    Output(component_id='store', component_property='data'),
    Output(component_id='store_in', component_property='children'),
    Output(component_id='upload-data', component_property='contents'),
    Input(component_id='save_ann', component_property='n_clicks'),
    Input(component_id='delete', component_property='n_clicks'),
    Input(component_id='upload-data', component_property='contents'),
    State(component_id='graph', component_property='figure'),
    State(component_id='store', component_property='data'),
    prevent_initial_call=True
)
def store_in(save_click, delete_click, upload_content, figure, store_data):
    # detect which button has been clicked
    trigger = callback_context.triggered[0]['prop_id']

    # actions depending on clicked button
    if trigger == "delete.n_clicks":
        return {}, {}, 'reset_upload_contents'

    elif trigger == 'upload-data.contents':
        annotations = parse_file(content=upload_content)
        return annotations, json.dumps(annotations, indent=1), 'reset_upload_contents'

    else:
        layout = figure['layout']
        annotations = layout.get('shapes', {})
        return annotations, json.dumps(annotations, indent=1), 'reset_upload_contents'


# retrieve annotations from dcc.Store
@ app.callback(
    Output(component_id='post', component_property='children'),
    Input(component_id='ret_ann', component_property='n_clicks'),
    State(component_id='store', component_property='data'),
    prevent_initial_call=True
)
def store_out(click, data):
    # create a gray dummy image
    dummy_image = np.ones((img.height, img.width)) * 220
    
    # create plotly express object
    figure = px.imshow(
        dummy_image,
        color_continuous_scale='gray',
    )

    # update figure layout
    figure.update_layout(layout)
    figure.update_coloraxes(showscale=False)

    # add annotations saved in dcc.Store
    if data:
        figure['layout'].update(shapes=data)

    # create dcc.Graph object
    graph = dcc.Graph(
        id='post_graph',
        figure=figure,
        # turn off plot interactivity
        config={'staticPlot': True}
    )
    return graph


# export data from dcc.Store into text file
@ app.callback(
    Output(component_id='dummy_out', component_property='children'),
    Input(component_id='export', component_property='n_clicks'),
    State(component_id='store', component_property='data'),
    prevent_initial_call=True
)
def export(click, data):
    # write annotations into text file
    with open(f'exported_annotations.txt', 'wt') as f:
        f.writelines(
            json.dumps(
                data,
                indent=1
            )
        )
    return


if __name__ == '__main__':
    app.run_server(debug=True, port=8053)
