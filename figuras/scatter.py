import pandas as pd
import plotly.express as px

def scatter_por_grupo(df, grupo):
    df_filtrado = df[df["Grupo"] == grupo]

    color = "firebrick" if grupo == "mayor pobreza" else "#0ae5f3"
    titulo = f"Conexiones fijas vs pobreza en las comunas con {grupo.lower()} en 2017"

    fig = px.scatter(
        df_filtrado,
        x="% conexiones por vivienda",
        y="% pobreza",
        text="Nombre comuna",
        custom_data=["Región","Nombre comuna", "Número de personas en situación de pobreza","% conexiones por vivienda", "% pobreza"],
        labels={
            "% conexiones por vivienda": "Conexiones fijas a internet por vivienda (%)",
            "% pobreza": "Personas en situación de pobreza (%)"
        },
        title=titulo
    )
    fig.update_traces(marker=dict(size=14, color=color), textposition="top center",
                      textfont=dict(
                            size=12,
                            color='black',
                            family='Helvetica'
                        ),
                      hovertemplate=
                        "<b>Región:</b>%{customdata[0]}<br>" +
                        "<b>Comuna:</b>%{customdata[1]}<br>" +
                        "<b>Número de personas en situación de pobreza:</b>%{customdata[2]}<br>" +
                        "<b>Porcentaje de conexiones:</b>%{customdata[3]:.2f}%<br>" +
                        "<b> Porcentaje de pobreza:</b>%{customdata[4]:.2f}%<br>" +
                        "<extra></extra>"  
    )
    
    
    fig.update_layout(title_font_size=15)

    return fig