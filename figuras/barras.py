import pandas as pd
import plotly.express as px

def barras_por_grupo(df, grupo):
    df_filtrado = df[df["Grupo"] == grupo].copy()
    df_long = pd.melt(
        df_filtrado,
        id_vars=["Nombre comuna"],
        value_vars=["% pobreza", "% conexiones por vivienda"],
        var_name="Indicador",
        value_name="Valor"
    )
    df_long["Indicador"] = df_long["Indicador"].replace({
        "% pobreza": "Pobreza (%)",
        "% conexiones por vivienda": "Conexiones a internet (%)"
    })

    titulo = f"Conexiones fijas vs pobreza en las comunas con {grupo.lower()} en 2017"
    color_map = {
    "Pobreza (%)": "firebrick",       
    "Conexiones a internet (%)": "#0ae5f3" 
    }
    fig = px.bar(
        df_long,
        x="Nombre comuna",
        y="Valor",
        color="Indicador",
        barmode="group",   
        labels={"Valor": "Porcentaje", "Nombre comuna": "Comuna"},
        title=titulo,
        text="Valor",
        color_discrete_map=color_map  
    )

    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig.update_layout(
        xaxis_tickangle=-45,
        yaxis=dict(range=[0, 100]), 
        title_font_size=15,
        legend_title_text="Indicador",
        margin=dict(t=50, b=150)
    )

    return fig