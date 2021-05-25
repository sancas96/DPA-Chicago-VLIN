#!/usr/bin/env python3

import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from general import *
from dash.dependencies import Input, Output

db_creds = get_database_connection('conf/local/credentials.yaml')
user = db_creds['user']
password = db_creds['password']
database = db_creds['database']
host = db_creds['host']
port = db_creds['port']

df=pd.DataFrame(query_database("SELECT * from monitoreo.restaurante_scores;"))
df.columns=[i[0] for i in query_database("SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS where table_name='restaurante_scores';")]

app = dash.Dash(__name__)

server = app.server

app.layout = html.Div([
    html.H1("Monitoreo Chicago"),
    dcc.Graph(id='graph'),
    html.Label([
        "Input Variable",
        dcc.Dropdown(
            id='column-dropdown', clearable=False,
            value = df.columns[2], options=[
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
    app.run_server(host='0.0.0.0',port=4321,debug=True)
