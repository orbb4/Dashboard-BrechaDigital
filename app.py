from dash import Dash, dcc, html, dash, Output, Input, callback
from figuras.bbplot import make_bbplot
from figuras.rankingbars import make_bchart
from data_loader import get_df_pop, get_df_rendimiento, get_df_internet, set_year
import pandas as pd
def get_df():
    df_pop = get_df_pop()
    df_rend = get_df_rendimiento()
    df_inter = get_df_internet()
    df_merged = df_rend.merge(df_pop, on="COD_REG_RBD")
    df_merged = df_merged.merge(df_inter, on="COD_REG_RBD")
    df_merged["CONEXIONES_POR_HABITANTE"] = (df_merged["NUM_CONEXIONES_FIJAS"] / df_merged["POP"]) *100
    return df_merged
df = get_df()
fig_bubble = make_bbplot(df)
fig_bars = make_bchart(df, 10)
#print(df_pop)
#print(df_rend)
app = Dash(__name__)
app.layout = html.Div([
    html.H1("Dashboard Brecha Digital"),
        dcc.Slider(
        id='year-slider',
        min=2002,
        max=2025,
        step=1,
        marks={str(year): str(year) for year in range(2002, 2025)},
        value=2018
    ),
    dcc.Graph(figure=fig_bubble, id="bbplot"),
    dcc.Graph(figure=fig_bars, id="barchart")
])
#ToDo: cargar todos los años de antemano (añadir AÑO al dataframe) para evitar lag
# eso y da algunos errores al moverse en el slider jeje
@callback(
    Output('bbplot', 'figure'),
    Input('year-slider', 'value'))
def update_bbchart(year):
    set_year(year)
    df = get_df()
    fig_bbplot =make_bbplot(df)
    return fig_bbplot
app.run(debug=True)