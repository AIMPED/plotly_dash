from dash import register_page, html, callback, Input, Output
from my_cache import open_file, FILE_LIST

# register page in the registry
register_page(__name__, path="/")

layout = html.Div(
    [
        html.Button('use data', id='btn_1'),
        html.Div(id='container_page_1')
    ]
)


@callback(
    Output('container_page_1', 'children'),
    Input('btn_1', 'n_clicks'),
    prevent_initial_call=True
)
def show_head(_):
    data = open_file(FILE_LIST[0])
    return data.head().to_json()

