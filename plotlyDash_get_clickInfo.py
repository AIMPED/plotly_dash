from dash import Dash, Input, Output, dcc, html
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import plotly.express as px
from PIL import Image
import urllib.request

# get an example image from url
urllib.request.urlretrieve(
    'https://raw.githubusercontent.com/michaelbabyn/plot_data/master/bridge.jpg',
    'bridge.jpg'
)

# open image and create plotly figure, locally stored images can be used this way too
img = Image.open('bridge.jpg')
fig = px.imshow(img=img)

# update figure layout, actually not necessary for the functionality
fig.update_layout(
    {
        'template': 'plotly_dark',
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        'width': img.width * 0.75,
        'height': img.height * 0.75,
        'xaxis': {'showgrid': False,
                  'showticklabels': False
                  },
        'yaxis': {'showgrid': False,
                  'showticklabels': False
                  }
    }
)

# initiate app, use a dbc theme
app = Dash(__name__,
           external_stylesheets=[dbc.themes.SLATE],
           meta_tags=[
               {'name': 'viewport',
                'content': 'width=device-width, initial-scale=1.0'
                }
           ]
           )

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H4('Click anywhere on the image'),
            dcc.Graph(id='graph', figure=fig),
        ], width={'size': 10}
        ),
        dbc.Col([
            html.H4('Coordinates of click'),
            html.Pre(id='click')
        ], width={'size': 2}
        )
    ])
], fluid=True)

# whenever possible, use clientside callbacks as they are much faster than server callbacks
# these callbacks have to be written in JS whereas the server callbacks can be written in python
app.clientside_callback(
    """
    function(clickData) {
        if (clickData == undefined) {
            throw window.dash_clientside.PreventUpdate;
        } else {
            var points = clickData.points[0]
            var x = points.x
            var y = points.y
            //var jsonstr = JSON.stringify(clickData, null, 2);
        }
        return [`x: ${x}\ny: ${y}`];
    }
     """, [Output('click', 'children')], [Input('graph', 'clickData')]
)

# serverside callback (python)
# @app.callback(Output('click', 'children'),
#               Input('graph', 'clickData')
#               )
# def get_click(clickData):
#     if not clickData:
#         raise PreventUpdate
#     else:
#         points = clickData.get('points')[0]
#         x = points.get('x')
#         y = points.get('y')

#     return f'x: {x}\ny: {y}'


if __name__ == '__main__':
    app.run_server(debug=True, port=8052)
