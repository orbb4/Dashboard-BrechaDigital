from dash import Dash, dcc, html, dash, Output, Input, callback
from figuras.bbplot import make_bbplot
from figuras.rankingbars import make_bchart
from data_loader import get_df_pop, get_df_rendimiento, get_df_internet, get_df_viviendas, set_year
import pandas as pd

def get_df():
    df_pop = get_df_pop()
    df_rend = get_df_rendimiento()
    df_inter = get_df_internet()
    df_vivi = get_df_viviendas()
    df_merged = df_rend.merge(df_pop, on="COD_REG_RBD")
    df_merged = df_merged.merge(df_inter, on="COD_REG_RBD")
    df_merged = df_merged.merge(df_vivi, on="COD_REG_RBD")
    #para revisar el df en caso de necesitar debug
    #df_merged.to_excel("soytesting.xlsx")
    df_merged["CONEXIONES_POR_VIVIENDA"] = (df_merged["NUM_CONEXIONES_FIJAS"] / df_merged["VIVIENDAS"]) *100
    return df_merged


df = get_df()
fig_bubble = make_bbplot(df)
fig_bars = make_bchart(df)
app = Dash(__name__)
app.layout = html.Div([
    html.H1("Dashboard Brecha Digital"),
    dcc.Dropdown(
        id='year-slider',
        options=[
            {'label': '2002', 'value': 2002},
            {'label': '2007', 'value': 2007},
            {'label': '2024', 'value': 2024},
        ],
        value=2024,
        clearable=False,
    ),
    html.Div([
    html.Div([dcc.Graph(figure=fig_bubble, id="bbplot")], style={"flex":"3"}),
    html.Div([dcc.Graph(figure=fig_bars, id="barchart")], style={"flex":"1"})    
    ], style={"display": "flex"})
])

@callback(
    Output('bbplot', 'figure'),
    Input('year-slider', 'value'))
def update_bbchart(year):
    set_year(year)
    df = get_df()
    fig_bbplot =make_bbplot(df)
    return fig_bbplot
app.run(debug=True)