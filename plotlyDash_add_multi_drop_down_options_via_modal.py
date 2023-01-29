import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, dcc, ctx, MATCH
import dash

# design of the modal
modal = html.Div(
    [
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Introduce new option")),
                dbc.ModalBody(
                    dcc.Input(
                        id={'type': 'input', 'index': idx},
                        type='text'
                    )
                ),
                dbc.ModalFooter(
                    children=[
                        dbc.Row(
                            dbc.Col(
                                dbc.ButtonGroup(
                                    [
                                        dbc.Button(
                                            "OK",
                                            id={'type': 'ok', 'index': idx},
                                            className="ms-auto",
                                            n_clicks=0
                                        ),
                                        dbc.Button(
                                            "Cancel",
                                            id={'type': 'cancel', 'index': idx},
                                            className="ms-auto",
                                            n_clicks=0
                                        )
                                    ]
                                )
                            )
                        )
                    ]
                )
            ],
            id={'type': 'modal', 'index': idx},
            is_open=False,
            centered=True
        ) for idx in range(3)
    ]
)

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.SLATE],
    meta_tags=[
        {'name': 'viewport',
         'content': 'width=device-width, initial-scale=1.0'
         }
    ]
)
app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dcc.Dropdown(
                    id={'type': 'drop', 'index': idx},
                    options=[1, 2, 3, 'create new'],
                    multi=True
                ) for idx in range(3)
            ]
        ),
        dbc.Row(
            [
                modal,
                html.Div(id={'type': 'dummy', 'index': 0})
            ]
        )
    ],
    fluid=True
)


@app.callback(
    Output({'type': 'modal', 'index': MATCH}, "is_open"),
    Output({'type': 'drop', 'index': MATCH}, 'options'),
    Output({'type': 'drop', 'index': MATCH}, 'value'),
    Input({'type': 'ok', 'index': MATCH}, "n_clicks"),
    Input({'type': 'cancel', 'index': MATCH}, "n_clicks"),
    Input({'type': 'drop', 'index': MATCH}, "value"),
    State({'type': 'drop', 'index': MATCH}, "options"),
    State({'type': 'input', 'index': MATCH}, 'value'),
    State({'type': 'modal', 'index': MATCH}, "is_open"),
    prevent_initial_call=True
)
def toggle_modal(ok, cancel, drop_value, drop_options, input_value, is_open):
    # which component has triggered the callback?
    trigger = ctx.triggered_id['type']

    # change of drop down value triggered
    if trigger == 'drop':
        if 'create new' in drop_value:
            # if 'create new', open modal
            return not is_open, drop_options, drop_value
        else:
            # if not 'create new', do nothing
            return is_open, drop_options, drop_value

    # ok button has been clicked
    if trigger == 'ok':
        # ok has been clicked, update the drop-down options
        new_options = [opt for opt in drop_options]
        new_options.insert(-1, input_value)
        new_values = [val for val in drop_value if val != 'create new']
        new_values.append(input_value)
        return not is_open, new_options, new_values

    # cancel button has been clicked
    if trigger == 'cancel':
        # cancel has been clicked, do not change options but return already selected to drop down value
        existing_values = [val for val in drop_value if val != 'create new']
        return not is_open, drop_options, existing_values


if __name__ == '__main__':
    app.run(debug=True, port=8051)
