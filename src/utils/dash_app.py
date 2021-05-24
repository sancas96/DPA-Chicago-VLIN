#!/usr/bin/env python3

import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

df=pd.read_csv("/home/luza/Downloads/restaurante_scores.csv")

app = dash.Dash(__name__)

server = app.server

app.layout = html.Div([
    html.H1("Monitoreo Chicago"),
    dcc.Graph(id='graph'),
    html.Label([
        "Input Variable",
        dcc.Dropdown(
            id='column-dropdown', clearable=False,
            value = df.columns[3], options=[
                {'label': c, 'value': c}
                for c in df.columns
            ])
    ]),
])
app.scripts.config.serve_locally=True

@app.callback(
    Output('graph', 'figure'),
    [Input("column-dropdown", "value")])

def update_figure(column):
    fig=px.histogram(
        df, y=column,
        facet_col="prediccion",
        histnorm="percent",
        color="entrenamiento",
        orientation="h",
        barmode="group",
        barnorm="percent",
        title="Establecimientos y sus predicciones",
        color_discrete_map={ # replaces default color mapping by value
                1: "Mediumvioletred", 0: "Darkgrey"
                },
        template="plotly_white"
    )
    fig.update_xaxes(title_text='Porcentaje')
    fig.update_layout(showlegend=False)
    
    return fig
# Run app and dis

if __name__ == '__main__':
    app.run_server(debug=True)
