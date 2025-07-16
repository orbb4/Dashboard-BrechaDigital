import plotly.express as px
import pandas as pd

def make_bchart(df, year=2024, top_n=16):
    if year>=2024:
        pruebas = ["MATE1_REG_ACTUAL", "MATE2_REG_ACTUAL", "HCSOC_REG_ACTUAL", "CIEN_REG_ACTUAL", "CLEC_REG_ACTUAL"]
    else:
        pruebas = ["MATE_ACTUAL", "HCSO_ACTUAL", "CIEN_ACTUAL", "LENG_ACTUAL"]
    df= df.melt(
        id_vars=["COD_REG_RBD", "CONEXIONES_POR_VIVIENDA", "POP"],
        value_vars=pruebas,
        var_name="TIPO_PRUEBA",
        value_name="PUNTAJE"
    )
    fig = aux_make_bchart(df, top_n)
    return fig


def aux_make_bchart(df, top_n):

    colors = {'MATE1_REG_ACTUAL':"rgb(255, 144, 14)",
               'MATE2_REG_ACTUAL':"rgb(132, 90, 204)",
                'CLEC_REG_ACTUAL':"rgb(50, 155, 170)",
                'CIEN_REG_ACTUAL':"rgb(44, 160, 101)",
                'HCSOC_REG_ACTUAL':"rgb(168, 84, 50)",
                
                'MATE_ACTUAL':"rgb(255, 144, 14)",
                'LENG_ACTUAL':"rgb(50, 155, 170)",
                'CIEN_ACTUAL':"rgb(44, 160, 101)",
                'HCSO_ACTUAL':"rgb(168, 84, 50)"
            }
    fig = px.bar(
        df,
        x="PUNTAJE",
        y="COD_REG_RBD",
        color="TIPO_PRUEBA",
        color_discrete_map=colors,
        labels={"PROM_GRAL": "Puntajes promedio", "COD_REG_RBD": "Región"},
        title="Mejores puntajes por región",
        orientation="h"
    )
    fig.update_layout(
        yaxis=dict(title="Región"),
        xaxis={"range":[1, 3500]}
    )
    return fig