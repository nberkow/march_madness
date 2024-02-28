from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import io
import base64
import plotly.express as px
import plotly.graph_objects as go

app = Dash(__name__)
server = app.server

app.layout = html.Div([
    html.Div([
        dcc.Graph(id="bracket"),
        dcc.Dropdown(['East', 'Midwest', 'South', 'West', 'Elite Eight', 'Full'], value='East', id='region-dropdown'),
        ])
    ])

@app.callback(
    Output('bracket','figure'),
    Input('region-dropdown','value')
)
def show_table_plot_and_slider(value):

    y_step = 1
    y_sep  = 1.5
    x_step = 1

    round = 3
    traces = []

    y_start = 0
    x_start = 0
    while round > 0:
        matchups = 2**round
        for m in range(matchups):
            y_points = [
                y_start, y_start, y_start + y_step, y_start + y_step
            ]
            x_points = [
                x_start, x_start + x_step, x_start + x_step, x_start
            ]
            traces.append(go.Scatter(y=y_points, x=x_points, line_color='purple', mode='lines', showlegend=False))
            y_start += (y_step * y_sep)
        round -= 1

    fig = go.Figure(traces)
    return(fig)


if __name__ == '__main__':
    app.run_server(debug=True)