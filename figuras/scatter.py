import pandas as pd
import plotly.express as px

def scatter_por_grupo(df, grupo):
    df_filtrado = df[df["Grupo"] == grupo]

    color = "firebrick" if grupo == "mayor pobreza" else "seagreen"
    titulo = f"Conexiones fijas vs pobreza en las comunas con {grupo.lower()} en el 2017"

    fig = px.scatter(
        df_filtrado,
        x="% conexiones por vivienda",
        y="% pobreza",
        text="Nombre comuna",
        labels={
            "% conexiones por vivienda": "Porecentaje de conexiones fijas a internet por vivienda",
            "% pobreza": "Porcentaje de pobreza"
        },
        title=titulo
    )
    fig.update_traces(marker=dict(size=12, color=color), textposition="top center")
    fig.update_layout(title_font_size=15)

    return fig