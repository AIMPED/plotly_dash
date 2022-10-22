import dash
from dash import Input, Output, State, html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd


# class for extracting information from the plotly.graph_object Figure()
class TraceInfo:
    def __init__(self, figure):
        self.fig = figure
        self.traces = self.__traces()
        self.number = self.__len__()
        self.names = self.__trace_names()
        self.colors = self.__trace_colors()

    def __getitem__(self, index):
        return self.traces[index]

    def __len__(self):
        return len(self.traces)

    def __traces(self):
        return self.fig.get('data', [])

    def __trace_colors(self):
        return [trace.get('marker', {}).get('color') for trace in self.traces]

    def __trace_names(self):
        return [trace.get('name') for trace in self.traces]


# RAW data
df = {'col1': [12, 15, 25, 33, 26, 33, 39, 17, 28, 25],
      'col2': [35, 33, 37, 36, 36, 26, 31, 21, 15, 29],
      'col3': [16, 4, 37, 36, 36, 32, 21, 21, 9, 29],
      'col4': [7, 21, 37, 10, 36, 24, 7, 21, 9, 6],
      'col5': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
      }

# create DataFrame
df = pd.DataFrame(df)

# create app, layout
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
    html.Div(
        [
            dcc.Dropdown(
                id='feature-choice',
                options=df.columns.values[0:4],
                multi=True,
                clearable=True,
                value=[]
            ),
            dcc.Graph(
                id='dynamic-graph',
                figure={}
            ),
        ],
        style={'width': '50%'}
    ),
    style={
        'display': 'flex',
        'justify-content': 'center',
        'align-items': 'center'
    },
)


@app.callback(
    Output('dynamic-graph', 'figure'),
    Input('feature-choice', 'value'),
    State('dynamic-graph', 'figure'),
    prevent_initial_call=True
)
def update_output(selection, current_figure):
    # on first selection of values or if values have been selected and deleted
    if not current_figure or len(current_figure.get('data')) == 0:
        # create figure for the initila selection, color is always red
        column = selection[0]
        trace = go.Scatter(
            x=df[column],
            y=df.col5,
            mode='lines',
            marker={'color': 'red'},
            name=column
        )
        return go.Figure(data=trace, layout={'showlegend': True})

    # this code is executed, if there is a current figure with at least one
    # trace in it.

    # set fixed color map
    color_map = ['red', 'blue', 'black', 'yellow']

    # get trace info
    t = TraceInfo(current_figure)
    current_traces = t.traces

    # differences between current selection and current figure. The trace names correspond
    # to the column names. This has to be guaranteed.
    existing = set(t.names)
    selected = set(selection)

    # decide what to do, which traces to keep, to delete and which to create
    keep = existing & selected
    delete = existing ^ keep
    new = keep ^ selected

    # get indices of traces to delete
    d_index = [t.names.index(d) for d in delete]

    # get the indices of the trace color which are kept
    # Trace names and colors have the same indices
    c_index = [t.names.index(k) for k in keep]

    # now that we have the index of the colors, we need to know the color name
    used_colors = {t.colors[i] for i in c_index}

    # usable colors are the colors of the initial color map
    # minus the colors which are already used by traces kept
    usable_colors = iter(
        sorted(
            list(used_colors ^ set(color_map)),
            key=color_map.index
        )
    )

    # delete traces to be deleted from current traces
    # sort the indices in descending order
    for i in sorted(d_index, reverse=True):
        current_traces.pop(i)

    # create new traces
    new_traces = []
    for column in new:
        new_traces.append(
            go.Scatter(
                x=df[column],
                y=df.col4,
                mode='lines',
                marker={'color': next(usable_colors)},
                name=column
            )
        )
    # create figure with current traces +  the new ones
    return go.Figure(data=current_traces + new_traces, layout={'showlegend': True})


if __name__ == '__main__':
    app.run(debug=True, port=8051)
