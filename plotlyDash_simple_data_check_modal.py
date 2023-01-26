import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, dcc, ctx
import dash

# design of the modal
modal = html.Div(
    [
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Header")),
                dbc.ModalBody("Confirm or cancel"),
                dbc.ModalFooter(
                    children=[
                        dbc.ButtonGroup(
                            [
                                dbc.Button(
                                    "OK",
                                    id="ok",
                                    className="ms-auto",
                                    n_clicks=0
                                ),
                                dbc.Button(
                                    "Cancel",
                                    id="cancel",
                                    className="ms-auto",
                                    n_clicks=0
                                )
                            ]
                        )
                    ]
                ),
            ],
            id="modal",
            is_open=False,
            centered=True
        ),
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
app.layout = html.Div(
    [
        dbc.Button(
            "add data",
            id="open",
            n_clicks=0
        ),
        dcc.Input(id='added_data', type='text'),
        # ^^ simulate the new data via input
        dcc.Store(id='stored_data', data='initial value'),
        html.Div(id='message'),
        html.Div(id='store_content'),
        modal
    ]
)


@app.callback(
    [
        Output("modal", "is_open"),
        Output("message", "children"),
        Output("ok", "disabled"),
        Output('stored_data', 'data')
    ],
    [
        Input("open", "n_clicks"),
        Input("ok", "n_clicks"),
        Input("cancel", "n_clicks"),
    ],
    [
        State("modal", "is_open"),
        State("added_data", "value"),
        State("ok", "disabled"),
        State('stored_data', 'data')
    ],
    prevent_initial_call=True
)
def toggle_modal(open_modal, ok, cancel, is_open, added_data, status_ok_btn, current_store_data):
    # which button triggered the callback?
    trigger = ctx.triggered_id

    # new data has been added
    if trigger == 'open':
        # check data. This is just a string comparison, but it could be any check.
        if added_data != 'correct data':
            # if not correct, set disabled=True for the OK button
            return not is_open, 'just opened', True, current_store_data
        else:
            # if correct, set disabled=False (button is clickable) for the OK button
            return not is_open, 'just opened', False, current_store_data

    # ok button has been clicked
    if trigger == 'ok':
        # ok has been clicked, update the dcc.Store() with the added data
        return not is_open, 'you just confirmed', status_ok_btn, added_data

    # cancel button has been clicked
    if trigger == 'cancel':
        # cancel has been clicked, do nothing
        return not is_open, 'you just canceled', status_ok_btn, current_store_data


@app.callback(
    Output('store_content', 'children'),
    Input('stored_data', 'data'),
)
def show_data(data):
    return data


if __name__ == '__main__':
    app.run(debug=True, port=8051)