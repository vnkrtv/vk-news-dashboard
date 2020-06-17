import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from dash.dependencies import Input, Output, State


app = dash.Dash(
    'VK News',
    meta_tags=[{"name": "viewport", "content": "width=device-width"}],
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    serve_locally=True
)


server = app.server

app.layout = dbc.Alert(
    "Hello, Bootstrap!", className="m-5"
)
if __name__ == "__main__":
    app.run_server(debug=True)
