from dash import register_page, html, callback, Input, Output
from my_cache import open_file, FILE_LIST

# register page in the registry
register_page(__name__, path="/page_2")

layout = html.Div(
    [
        html.Button('use data', id='btn_2'),
        html.Div(id='container_page_2')
    ]
)


@callback(
    Output('container_page_2', 'children'),
    Input('btn_2', 'n_clicks'),
    prevent_initial_call=True
)
def show_head(_):
    data = open_file(FILE_LIST[1])
    return data.head().to_json()


