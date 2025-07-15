import plotly.express as px
import plotly.express as px
def make_bchart(df, top_n=5):
    df_sorted =  df.sort_values("PROM_GRAL", ascending=False).head(top_n)
    df_sorted = df.sort_values("PROM_GRAL", ascending=False).head(top_n).copy()
    df_sorted["COD_REG_RBD"] = df_sorted["COD_REG_RBD"].astype(str) 
    fig = px.bar(
        df_sorted,
        x="PROM_GRAL",
        y="COD_REG_RBD",
        labels={"PROM_GRAL": "Promedio Académico", "COD_REG_RBD": "Región"},
        title="Regiones por mejor promedio académico",
        orientation="h"
    )
    fig.update_layout(
        yaxis={'categoryorder':'total ascending'},
        xaxis=dict(title="Promedio académico", range=[1,7])
    )
    return fig