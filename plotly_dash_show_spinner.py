import dash
from dash import html, dcc, Input, Output
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import time

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SOLAR])
app.layout = html.Div(
    [
        dbc.Button(
            'Click this button to show the spinner',
            id='button'
        ),
        dcc.Input(
            id='input',
            type='text',
            value='try to change this text while spinner is showing',
            style={'width': '50%'}
        ),
        dbc.Spinner(
            id='loading-1',
            type='border',
            color='rgb(181,137,0)',
            spinner_style={'width': '8rem', 'height': '8rem'},
            fullscreen=True,
            fullscreen_style={'backgroundColor': 'rgba(0,0,0,0.4)'},
            # the children ID defines the action for which the spinner is shown
            # in this case it is the dummy output
            children=html.Pre(id='dummy_out')
        )
    ]
)


@app.callback(
    Output('dummy_out', 'children'),
    Input('button', 'n_clicks'),
    prevent_initial_call=True
)
def update_output(click):
    if not click:
        raise PreventUpdate
    else:
        time.sleep(5)
        return 'you had to wait 5 seconds'


if __name__ == '__main__':
    app.run_server(debug=True, port=8051)
