import pandas as pd
import plotly.express as px

def barras_por_grupo(df, grupo):
    df_filtrado = df[df["Grupo"] == grupo].copy()
    df_long = pd.melt(
        df_filtrado,
        id_vars=["Nombre comuna", "Región", "Número de personas en situación de pobreza", "Número conexiones fijas"],
        value_vars=["% pobreza", "% conexiones por vivienda"],
        var_name="Indicador",
        value_name="Valor"
    )
    df_long["Indicador"] = df_long["Indicador"].replace({
        "% pobreza": "Pobreza (%)",
        "% conexiones por vivienda": "Conexiones a internet (%)"
    })
    
    #datos para la etiqueta
    df_long["custom_data"] = df_long[[
        "Región",
        "Nombre comuna",
        "Número de personas en situación de pobreza",
        "Número conexiones fijas",
        "Indicador",
        "Valor"
    ]].values.tolist()

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

    for trace, indicador in zip(fig.data, df_long["Indicador"].unique()):
        sub_df = df_long[df_long["Indicador"] == indicador].reset_index(drop=True)
        trace.customdata = sub_df[[
            "Región",
            "Nombre comuna",
            "Número de personas en situación de pobreza",
            "Número conexiones fijas",
            "Indicador",
            "Valor"
        ]].values
        if indicador == "Pobreza (%)":
            trace.hovertemplate = (
                "<b>Región:</b> %{customdata[0]}<br>" +
                "<b>Comuna:</b> %{customdata[1]}<br>" +
                "<b>Número de personas en situación de pobreza:</b> %{customdata[2]}<br>" +
                "<b>Porcentaje de pobreza:</b> %{customdata[5]:.2f}%<br>" +
                "<extra></extra>"
            )
        elif indicador == "Conexiones a internet (%)":
            trace.hovertemplate = (
                "<b>Región:</b> %{customdata[0]}<br>" +
                "<b>Comuna:</b> %{customdata[1]}<br>" +
                "<b>Total de conexiones fijas:</b> %{customdata[3]}<br>" +
                "<b>Conexiones a internet por vivienda:</b> %{customdata[5]:.2f}%<br>" +
                "<extra></extra>"
            )


    fig.update_traces(
        texttemplate='%{text:.1f}%',
        textposition='outside',
    )
    fig.update_layout(
        xaxis_tickangle=-45,
        yaxis=dict(range=[0, 100]), 
        title_font_size=15,
        legend_title_text="Indicador",
        margin=dict(t=50, b=150)
    )

    return fig