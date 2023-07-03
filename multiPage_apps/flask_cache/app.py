import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
from my_cache import cache, CACHE_CONFIG, FILE_LIST, open_file


meta_tags = [{"name": "viewport", "content": "width=device-width, initial-scale=1.0"}]

external_stylesheets = [
    dbc.themes.SLATE,
    dbc.icons.FONT_AWESOME,
]

# initiate app
app = dash.Dash(
    __name__,
    use_pages=True,
    meta_tags=meta_tags,
    suppress_callback_exceptions=True,
    external_stylesheets=external_stylesheets,
)

# this line is needed if waitress is used as WSGI server
server = app.server

# initialize caching
cache.init_app(server, config=CACHE_CONFIG)

# create a navbar. Includes logo, theme switch and menu drop down
navbar = dbc.Navbar(
    id='navbar',
    children=[
        dbc.NavbarBrand(
            html.A(
                [
                    html.I(
                        # className="bi bi-github d-inline",
                        className="fa-brands fa-github d-inline",
                        style={'color': 'white', 'height': '50px'}
                    ),
                ],
                href="https://github.com/AIMPED",
                target="_blank",
                className='align-items-center text-decoration-none text-black',
            ),
            className="me-auto",  # me-auto pushes other elements to the right
            style={"margin-left": "10px"},

        ),
        dbc.Nav(
            dbc.DropdownMenu(
                [
                    dbc.DropdownMenuItem(
                        children=page['name'],
                        href=page['path']
                    )
                    for page in dash.page_registry.values()
                    if page['name'] != 'Not found 404'
                ],
                align_end=True,
                label='Menu',
                color='primary',
                style={'marginLeft': '15px'},
            ),
            navbar=True,
        ),
    ],
    color='primary',
    className='mb-0',
    # ^^ no margin on bottom
    style={'height': '50px'}
)

app.layout = html.Div(
    [
        navbar,
        dash.page_container,
        dcc.Store(id='central_store')
    ],
)


# callback at app startup to memoize the data
@callback(
    Output('central_store', 'data'),
    Input('central_store', 'data'),
)
def memo_call(_):
    for url in FILE_LIST:
        _ = open_file(url)
    return {}


if __name__ == "__main__":
    app.run(debug=True, port=8055)
