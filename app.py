from dash import Dash, dcc, html, dash, Output, Input, callback
from figuras.bbplot import make_bbplot
from figuras.rankingbars import make_bchart
from data_loader import get_df_pop, get_df_rendimiento, get_df_internet, get_df_viviendas, get_df_prueba, get_df_pobreza, set_year
import pandas as pd
regiones_dict = {
    1: "Tarapacá",
    2: "Antofagasta",
    3: "Atacama",
    4: "Coquimbo",
    5: "Valparaíso",
    6: "O'Higgins",
    7: "Maule",
    8: "Biobío",
    9: "La Araucanía",
    10: "Los Lagos",
    11: "Aysén",
    12: "Magallanes",
    13: "Metropolitana",
    14: "Los Ríos",
    15: "Arica y Parinacota",
    16: "Ñuble"
}
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
    df_merged["REGION_NOMBRE"] = df_merged["COD_REG_RBD"].map(regiones_dict)
    return df_merged


current_prueba = "MATE1_REG_ACTUAL"
pruebas_paes=['M1', 'M2', 'HISTORIA', 'LENGUAJE', 'CIENCIAS']
pruebas_psuptu=['MATEMATICA', 'HISTORIA', 'LENGUAJE', 'CIENCIAS']
pruebas = pruebas_paes
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
                2007: '2007',
                2017: '2017',
                2024: '2024'
            },
            value=2024,
            step=None
        ),
        # esto es una fila (2 visualizaciones)
        html.Div([
            html.Div([
                dcc.Dropdown(pruebas, value='M1', id='prueba-dropdown'),
                dcc.Graph(figure=fig_bubble, id="bbplot", style={"flexGrow": 1})
            ], style={"flexGrow": 1, "flex": 2.5, "display": "flex", "flexDirection": "column", "minHeight": "0", "padding": "2%"}),
            html.Div([
                dcc.Graph(figure=fig_bars, id="barchart", style={"flexGrow": 1})
            ], style={"display": "flex", "flex":1.5, "minHeight": "0", "flexDirection": "column", "padding": "2%"})    
        ], style={"display": "flex", "height": "70vh", "minHeight": "0"})
    ], style={"backgroundColor": "#ffffff", "padding": "1%", "borderRadius": "10px", "minHeight": "80vh", "margin": "1%"}),
    # fin de la fila
    html.Div([
        html.Img(src="/assets/wordcloud.png", style={
            "display": "block",
            "marginLeft": "auto",
            "marginRight": "auto",
            "maxWidth": "100%",
            "height": "100%"
        })
    ], style={"backgroundColor": "#ffffff", "padding": "1%", "borderRadius": "10px", "minHeight": "40vh", "margin": "1% auto", "maxWidth": "30%", "maxHeigth": "40%"})
], style={"backgroundColor": "#e9e9e9"})

@callback(
    Output('barchart', 'figure'),
    Input('year-slider', 'value'),
)
def update_bars(year):
    set_year(year)
    fig = make_bchart(get_df(), year)
    return fig




@callback(
    Output('bbplot', 'figure'),
    Input('year-slider', 'value'),
    Input('prueba-dropdown', 'value')
)
def update_bbchart(year, prueba):
    global current_prueba
    es_paes = False
    set_year(year)
    if year>=2024:
        es_paes=True
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
    else:
        if prueba=="MATEMATICA":
            current_prueba="MATE_ACTUAL"
        elif prueba == "HISTORIA":
            current_prueba = "HCSO_ACTUAL"
        elif prueba == "HISTORIA":
            current_prueba = "HCSO_ACTUAL"
        elif prueba=="CIENCIAS":
            current_prueba="CIEN_ACTUAL"
        elif prueba=="LENGUAJE":
            current_prueba="LENG_ACTUAL"
    df = get_df()
    fig_bbplot =make_bbplot(df, current_prueba, prueba, es_paes)
    return fig_bbplot

@callback(
    Output('prueba-dropdown', "options"),
    Output('prueba-dropdown', "value"),
    Input("year-slider", "value")
)
def update_dropdown(year):
    default_value = "M1"
    if year>=2024:
        pruebas = pruebas_paes
    else:
        pruebas=pruebas_psuptu
        default_value = "MATEMATICA"
    return pruebas, default_value


app.run(debug=True)