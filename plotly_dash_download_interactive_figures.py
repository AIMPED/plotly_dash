from dash import Dash, Input, Output, State, dcc, html
import plotly.graph_objects as go
import numpy as np
import zipfile
import io

app = Dash()

app.layout = html.Div(
    [
        dcc.Dropdown(
            id='drop',
            options=[
                {'label': 'graph1', 'value': 'fig1'},
                {'label': 'graph2', 'value': 'fig2'}
            ],
            multi=True
        ),
        html.Button('Download selection', id='btn'),
        dcc.Graph(
            id='graph1',
            figure=go.Figure(
                go.Scatter(
                    x=np.random.randint(0, 10, 100),
                    y=np.random.randint(0, 10, 100),
                    marker={'color': 'pink'},
                    mode='markers',
                    name='fig1'
                )
            )
        ),
        dcc.Graph(
            id='graph2',
            figure=go.Figure(
                go.Scatter(
                    x=np.random.randint(0, 10, 100),
                    y=np.random.randint(0, 10, 100),
                    marker={'color': 'blue'},
                    mode='markers',
                    name='fig2'
                )
            )
        ),
        dcc.Download(id='down'),
    ]
)


@app.callback(
    Output('down', 'data'),
    Input('btn', 'n_clicks'),
    State('drop', 'value'),
    State('graph1', 'figure'),
    State('graph2', 'figure'),
    prevent_initial_call=True
)
# adapted from: https://stackoverflow.com/questions/67917360/plotly-dash-download-bytes-stream/67918580#67918580
def func(_, selection, *figures):
    to_download = check_state(selection, figures)

    def write_archive(bytes_io):
        with zipfile.ZipFile(bytes_io, mode="w") as zf:
            for idx, fig in enumerate(to_download):
                go_fig = go.Figure(fig)
                buf = io.StringIO()
                go_fig.write_html(buf)
                img_name = f'fig_{idx}.html'
                zf.writestr(img_name, buf.getvalue())
    return dcc.send_bytes(write_archive, "app_download.zip")


def check_state(selection, figures):
    return [fig for fig in figures if extract_name(fig) in selection]


def extract_name(figure):
    return figure.get('data', [])[0].get('name')


if __name__ == '__main__':
    app.run(debug=True, port=8051)
