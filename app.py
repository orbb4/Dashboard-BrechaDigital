from dash import Dash, dcc, html, dash, Output, Input, callback
from figuras.bbplot import make_bbplot
from figuras.rankingbars import make_bchart
from figuras.heatMapTasaMatricula import make_heatmapMatriculas
from figuras.heatMapConexiones import make_heatmapConexiones
from figuras.scatter import scatter_por_grupo
from figuras.barras import barras_por_grupo
from data_loader import get_df_pop, get_df_rendimiento, get_df_internet, get_df_viviendas, get_df_prueba, get_df_pobreza, set_year
import pandas as pd


fig_heatmapMatriculas = make_heatmapMatriculas()
fig_heatmapConexiones = make_heatmapConexiones()

#para scatter
df_conexionesPobreza = pd.read_csv("Dataset/conexionVsPobreza.csv")
df_mas_pobreza = df_conexionesPobreza[df_conexionesPobreza["Grupo"] == "mayor pobreza"]
df_menos_pobreza = df_conexionesPobreza[df_conexionesPobreza["Grupo"] == "menor pobreza"]
fig_scatter_mas = scatter_por_grupo(df_mas_pobreza, "mayor pobreza")
fig_scatter_menos = scatter_por_grupo(df_menos_pobreza, "menor pobreza")
#para barras
fig_barras_mas = barras_por_grupo(df_mas_pobreza, "mayor pobreza")
fig_barras_menos = barras_por_grupo(df_menos_pobreza, "menor pobreza")
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

df_by_year = {}
for year in [2007, 2017, 2024]:
    set_year(year)
    df = get_df()
    df_by_year[year] = df
df = get_df()

fig_bubble = make_bbplot(df, current_prueba)
fig_bars = make_bchart(df)
app = Dash(__name__)
app.layout = html.Div([
    html.H1(
        "Dashboard Brecha Digital Educativa",
        style={
            "textAlign": "center",         
            "color": "#ffffff",           
            "fontSize": "36px",            
            "fontFamily": "Segoe UI, sans-serif",  
            "marginTop": "20px",
            "marginBottom": "20px",
            "textShadow": "1px 1px 2px #ccc"  
        }
    ),
    html.P(
        "Este dashboard muestra la evolución y distribución regional de la brecha digital educativa en Chile,"
        " enfocándose en el acceso a la educación superior."
        " Se analiza la tasa de matrícula, conexiones a internet por habitante, y rendimiento promedio en las pruebas de acceso en los años 2007, 2017 y 2024, así como la tasa de pobreza en determinadas comunas.",
        style={"textAlign": "center", "fontSize": "16px", "color": "#fff", "maxWidth": "800px", "margin": "0 auto 30px auto"}
    ),
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
        html.Div([
                dcc.Graph(figure=fig_heatmapMatriculas, id="heatmap1", style={
                "width": "500px",        
                "margin": "0 auto"
            })
            ], style={
                "margin": "1%", 
                "padding": "1%", 
                "backgroundColor": "#ffffff", 
                "borderRadius": "10px",
                "flex": "1"
            }),

            html.Div([
                dcc.Graph(figure=fig_heatmapConexiones, id="heatmap2", style={
                "width": "500px",        
                "margin": "0 auto"
            })
            ], style={
                "margin": "1%", 
                "padding": "1%", 
                "backgroundColor": "#ffffff", 
                "borderRadius": "10px",
                "flex": "1"
            })
        ], style={
            "display": "flex",
            "flexDirection": "row",
            "justifyContent": "space-around",
            "backgroundColor": "#0a0954"}),
    html.Div([
        # Grupo mayor pobreza
        html.Div([
            dcc.RadioItems(
                id="tipo-grafico-mas",
                options=[
                    {"label": "Scatter", "value": "scatter"},
                    {"label": "Barras", "value": "barras"}
                ],
                value="scatter",
                inline=True,
                labelStyle={"marginRight": "30px"},  
                style={"marginBottom": "10px"}
            ),
            dcc.Graph(id="grafico-mas", style={'height': '500px'})
        ], style={
            "margin": "1%", "padding": "1%", "backgroundColor": "#ffffff", "borderRadius": "10px", "flex": "1"
        }),

        # Grupo menor pobreza
        html.Div([
                dcc.RadioItems(
                id="tipo-grafico-menos",
                options=[
                    {"label": "Scatter", "value": "scatter"},
                    {"label": "Barras", "value": "barras"}
                ],
                value="scatter",
                inline=True,
                labelStyle={"marginRight": "30px"}, 
                style={"marginBottom": "10px"}
            ),
            dcc.Graph(id="grafico-menos", style={'height': '500px'})
        ], style={
            "margin": "1%", "padding": "1%", "backgroundColor": "#ffffff", "borderRadius": "10px", "flex": "1"
        }),
    ], style={
        "display": "flex",
        "flexDirection": "row",
        "justifyContent": "space-around",
        "backgroundColor": "#0a0954"
    }),
    html.Div([
        html.H2("Palabras más utilizadas en informe: Brecha Digital e Inclusión 17/04/2023", style={
        "textAlign": "center",
        "marginBottom": "10px",
        "color": "#333333"
        }),
        html.Img(src="/assets/wordcloud.png", style={
            "display": "block",
            "marginLeft": "auto",
            "marginRight": "auto",
            "maxWidth": "100%",
            "height": "100%"
        })
    ], style={"backgroundColor": "#ffffff", "padding": "1%", "borderRadius": "10px", "minHeight": "40vh", "margin": "1% auto", "maxWidth": "30%", "maxHeigth": "40%"})
], style={"backgroundColor": "#0a0954"})

@callback(
    Output('barchart', 'figure'),
    Input('year-slider', 'value'),
)
def update_bars(year):
    df = df_by_year[year]
    fig = make_bchart(df, year)
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
    df = df_by_year[year]
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

@app.callback(
    Output("grafico-mas", "figure"),
    Input("tipo-grafico-mas", "value")
)
def update_grafico_mas(tipo):
    if tipo == "scatter":
        return fig_scatter_mas
    else:
        return fig_barras_mas

@app.callback(
    Output("grafico-menos", "figure"),
    Input("tipo-grafico-menos", "value")
)
def update_grafico_menos(tipo):
    if tipo == "scatter":
        return fig_scatter_menos
    else:
        return fig_barras_menos


comunas_mas_pobreza, comunas_menos_pobreza = get_df_pobreza()
comunas_mas_pobreza.to_csv("comunas_mas_pobreza.csv", index=False, encoding="utf-8")
comunas_menos_pobreza.to_csv("comunas_menos_pobreza.csv", index=False, encoding="utf-8")
app.run(debug=True)