# this is an answer to a question on the plotly forums
# https://community.plotly.com/t/creating-an-overview-plot-of-another-one-using-to-image/71416

from dash import Dash, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import numpy as np

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Button(id='btn', children='new data')
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(id='fig-main')
                ),
                dbc.Col(
                    dcc.Graph(id='fig-overview'),
                )
            ]
        ),
        dcc.Store(id='initial_figure_range'),
    ],
    fluid=True
)

# this callback gets triggered at startup. The Output('fig-main', 'relayoutData') is necessary
# because the relayoutData is not reset automatically when creating a new figure
@app.callback(
    Output('fig-main', 'figure'),
    Output('initial_figure_range', 'data'),
    Output('fig-main', 'relayoutData'),
    Input('btn', 'n_clicks'),
)
def create_new_figure(_):
    # create base figure
    fig = px.scatter(
        x=np.random.sample(150),
        y=np.random.sample(150),
        color=np.random.randint(0, 3, 150)
    ).update_layout(height=500, width=800)

    # extract ranges. It would be better not to use full_figure_for_development()
    # and use a clientside callback instead
    xrange = fig.full_figure_for_development().layout.xaxis.range
    yrange = fig.full_figure_for_development().layout.yaxis.range
    return fig, {'x': xrange, 'y': yrange}, None  # reset relayoutData


app.clientside_callback(
    """
    function(re_layout, initial_range, fig) {
        if (re_layout == null) {
            x = initial_range.x
            y = initial_range.y
        } else {
            // this should be improved. I did not know how to check properly the content of the relayoutData 
            if ("xaxis.range[0]" in re_layout) {
                x = [re_layout["xaxis.range[0]"], re_layout["xaxis.range[1]"]]
                y = [re_layout["yaxis.range[0]"], re_layout["yaxis.range[1]"]]
            } else {
                x = initial_range.x
                y = initial_range.y
            }
        }

        // create new figure
        newFig = JSON.parse(JSON.stringify(fig))

        // the State() of the figure actually shows the axis ranges after zooming
        // set the axis ranges to the initial values
        newFig.layout.xaxis.range = initial_range.x
        newFig.layout.yaxis.range = initial_range.y

        // delete any existing shape
        newFig['layout']['shapes'] = []

        // add rectangular shape for overview
        newFig['layout']['shapes'] = [{
            'editable': true,
            'xref': 'x',
            'yref': 'y',
            'layer': 'above',
            'opacity': 1,
            'line': {
                'color': 'red',
                'width': 1,
                'dash': 'solid'
            },
            'fillcolor': 'rgba(1, 0, 0, 0.2',
            'fillrule': 'evenodd',
            'type': 'rect',
            'x0': x[0],
            'y0': y[0],
            'x1': x[1],
            'y1': y[1]
        }]
        return newFig
    }
    """,
    Output('fig-overview', 'figure'),
    Input('fig-main', 'relayoutData'),
    Input('initial_figure_range', 'data'),
    State('fig-main', 'figure'),
    prevent_initial_call=True
)

if __name__ == '__main__':
    app.run_server(debug=True)
