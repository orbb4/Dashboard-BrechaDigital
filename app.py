from dash import Dash, dcc, html, dash, Output, Input, callback
from figuras.bbplot import make_bbplot
from figuras.rankingbars import make_bchart
from data_loader import get_df_pop, get_df_rendimiento, get_df_internet, get_df_viviendas, get_df_prueba, set_year
import pandas as pd

def get_df():
    df_pop = get_df_pop()
    df_rend = get_df_rendimiento()
    df_inter = get_df_internet()
    df_vivi = get_df_viviendas()
    df_prueba = get_df_prueba()
    df_merged = df_rend.merge(df_pop, on="COD_REG_RBD")
    df_merged = df_merged.merge(df_inter, on="COD_REG_RBD")
    df_merged = df_merged.merge(df_vivi, on="COD_REG_RBD")
    df_merged = df_merged.merge(df_prueba, on="COD_REG_RBD")
    df_merged["CONEXIONES_POR_VIVIENDA"] = (df_merged["NUM_CONEXIONES_FIJAS"] / df_merged["VIVIENDAS"]) *100
    return df_merged


current_prueba = "MATE1_REG_ACTUAL"
df = get_df()
fig_bubble = make_bbplot(df, current_prueba)
fig_bars = make_bchart(df)
app = Dash(__name__)
app.layout = html.Div([
    html.H1("Dashboard Brecha Digital"),
    html.Div([
        dcc.Slider(
            id='year-slider',
            marks={
                2002: '2002',
                2007: '2007',
                2017: '2017',
                2024: '2024'
            },
            value=2024,
            step=None
        ),
        html.Div([
            html.Div([
                dcc.Dropdown(['M1', 'M2', 'HISTORIA', 'LENGUAJE', 'CIENCIAS'], value='M1', id='prueba-dropdown'),
                dcc.Graph(figure=fig_bubble, id="bbplot", style={"flexGrow": 1})
            ], style={"flexGrow": 1, "flex": 3, "display": "flex", "flexDirection": "column", "minHeight": "0", "padding": "2%"}),
            html.Div([
                dcc.Graph(figure=fig_bars, id="barchart", style={"flexGrow": 1})
            ], style={"display": "flex", "flex":1, "minHeight": "0", "flexDirection": "column", "padding": "2%"})    
        ], style={"display": "flex", "height": "70vh", "minHeight": "0"})
    ], style={"backgroundColor": "#ffffff", "padding": "1%", "borderRadius": "10px", "minHeight": "80vh", "margin": "1%"}),
], style={"backgroundColor": "#e9e9e9"})

@callback(
    Output('bbplot', 'figure'),
    Input('year-slider', 'value'),
    Input('prueba-dropdown', 'value')
)
def update_bbchart(year, prueba):
    global current_prueba
    set_year(year)
    if prueba=="M1":
        current_prueba="MATE1_REG_ACTUAL"
    elif prueba=="M2":
        current_prueba="MATE2_REG_ACTUAL"
    elif prueba=="HISTORIA":
        current_prueba="HCSOC_REG_ACTUAL"
    elif prueba=="CIENCIAS":
        current_prueba="CIEN_REG_ACTUAL"
    elif prueba=="LENGUAJE":
        current_prueba="CLEC_REG_ACTUAL"
    df = get_df()
    print(df.columns)
    print(df[current_prueba])
    fig_bbplot =make_bbplot(df, current_prueba, prueba)
    return fig_bbplot

app.run(debug=True)