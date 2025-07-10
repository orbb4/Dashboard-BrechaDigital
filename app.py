from dash import Dash, dcc, html, dash
from figuras.bbplot import make_bbplot
from figuras.rankingbars import make_bchart
from data_loader import get_df_pop, get_df_rendimiento, get_df_internet
import pandas as pd

df_pop = get_df_pop()
df_rend = get_df_rendimiento()
df_inter = get_df_internet()
df_merged = df_rend.merge(df_pop, on="COD_REG_RBD")
df_merged = df_merged.merge(df_inter, on="COD_REG_RBD")
df_merged["CONEXIONES_POR_HABITANTE"] = (df_merged["NUM_CONEXIONES_FIJAS"] / df_merged["POP"]) *100


fig_bubble = make_bbplot(df_merged)
fig_bars = make_bchart(df_merged, 10)
#print(df_pop)
#print(df_rend)
app = Dash(__name__)
app.layout = html.Div([
    html.H1("Dashboard Brecha Digital"),
    dcc.Graph(figure=fig_bubble),
    dcc.Graph(figure=fig_bars)
])


app.run(debug=True)