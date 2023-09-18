import json
import time
import os

from dash import Dash, DiskcacheManager, CeleryManager, Input, Output, html, callback
import dash_bootstrap_components as dbc

if 'REDIS_URL' in os.environ:
    # Use Redis & Celery if REDIS_URL set as an env variable
    from celery import Celery
    celery_app = Celery(__name__, broker=os.environ['REDIS_URL'], backend=os.environ['REDIS_URL'])
    background_callback_manager = CeleryManager(celery_app)

else:
    # Diskcache for non-production apps when developing locally
    import diskcache
    cache = diskcache.Cache("./cache")
    background_callback_manager = DiskcacheManager(cache)

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    background_callback_manager=background_callback_manager
)

# define the modal. In this case it only shows the progress bar and a cancel button
modal = dbc.Modal(
            [
                dbc.ModalHeader(
                    dbc.ModalTitle("Your progress bar"),
                    close_button=False
                    # ^^ important, otherwise the user can close the modal
                    #    but the callback will be running still
                ),
                dbc.ModalBody(
                    html.Progress(
                        id="progress_bar",
                        value="0",
                        style={'width': '100%'}
                    )
                ),
                dbc.ModalFooter(
                    dbc.Button(
                        "Cancel",
                        id="cancel_button_id",
                        className="ms-auto",
                        n_clicks=0
                    )
                )
            ],
            id="modal",
            is_open=False,
            backdrop="static",
            keyboard=False
            # ^^ important, otherwise the user can close the modal via the ESC button
            #    but the callback will be running still
        )

app.layout = html.Div(
    [
        html.Div(
            html.P(
                id="paragraph_id",
                children=["Button not clicked"]
            )
        ),
        html.Button(
            id="button_id",
            children="Run Job!"
        ),
        modal
    ]
)


@callback(
    output=Output("paragraph_id", "children"),
    inputs=Input("button_id", "n_clicks"),
    background=True,
    running=[
        (Output("button_id", "disabled"), True, False),
        (Output('modal', 'is_open'), True, False)
    ],
    progress=[
        Output("progress_bar", "value"),
        Output("progress_bar", "max")
    ],
    cancel=Input("cancel_button_id", "n_clicks"),
    prevent_initial_call=True
)
def update_progress(set_progress, _):
    total = 500
    just_a_list = []

    for i in range(total + 1):
        just_a_list.append(i)
        set_progress((str(i), str(total)))
        time.sleep(0.01)

    return json.dumps(just_a_list)


if __name__ == "__main__":
    app.run(debug=True)
