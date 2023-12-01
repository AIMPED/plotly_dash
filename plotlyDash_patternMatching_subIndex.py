import time
import dash
from dash import html, dcc, Input, Output, ALL, MATCH, ctx, State

# define amount of components
BUTTONS = 5
ROWS = 2


def create_lookup(major: int, minor: int) -> dict:
    """
    function creates a dictionary where the keys are a combination
    of major and minor indices and values are integers (sequential)

    Parameters:
        major: range of major indices
        minor: range of minor indices

    Returns:
        dictionary
    """
    look_up = {}
    count = 0
    for mjr in range(major):
        for mir in range(minor):
            key = f'{mjr}-{mir}'
            look_up[key] = count
            count += 1
    return look_up


def search(search_in: dict, search_for: str, search_what='major') -> list:
    """
    function searches in the keys of a dictionary for a string

    Parameters:
        search_in: dictionary in which to search
        search_for: search string
        search_what: first or second part of the key.spit('-')

    Returns:
        list of dict.values() where the search string has been found in dict.keys()
    """
    found = []
    for combined_index in search_in.keys():

        # split into major and minor index
        mjr, mnr = combined_index.split('-')

        # what is searched for?
        if search_what == 'major':
            if search_for == mjr:
                found.append(search_in[combined_index])
        else:
            if search_for == mnr:
                found.append(search_in[combined_index])

    return found


app = dash.Dash(__name__)

app.layout = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        html.Button(
                            id={'type': 'btn', 'index': f'{major}-{minor}'},
                            children=f'{major}-{minor}'
                        )
                        for minor in range(BUTTONS)
                    ]
                )
                for major in range(ROWS)
            ]
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            id={'type': 'out', 'index': f'{major}-{minor}'},
                            children=f'{major}-{minor}'
                        )
                        for minor in range(BUTTONS)
                    ]
                )
                for major in range(ROWS)
            ]
        ),
        dcc.Store(id='lookup', data=create_lookup(ROWS, BUTTONS))
    ]
)


@app.callback(
    Output({'type': 'out', 'index': MATCH}, 'children'),
    Input({'type': 'btn', 'index': MATCH}, 'n_clicks'),
    prevent_initial_call=True
)
def show(click):
    idx = ctx.triggered_id.index
    return f'index {idx} clicked {click} times'


@app.callback(
    Output({'type': 'out', 'index': ALL}, 'children', allow_duplicate=True),
    Input({'type': 'btn', 'index': ALL}, 'n_clicks'),
    State({'type': 'out', 'index': ALL}, 'children'),
    State('lookup', 'data'),
    prevent_initial_call=True
)
def show(_, state, lookup):
    # create some delay between the two callbacks
    time.sleep(1)

    # extract trigger
    idx = ctx.triggered_id.index

    # spit into major and minor indices
    row_idx, btn_index = idx.split('-')

    # find the positions of the corresponding indices
    indices = search(
        search_in=lookup,
        search_for=row_idx,
        search_what='major'
    )

    # change values where needed
    for i in indices:
        state[i] = f'all has been used. button in row {row_idx} triggered callback'

    return state


if __name__ == '__main__':
    app.run_server(debug=True)
