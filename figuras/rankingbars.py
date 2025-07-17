import plotly.express as px
import pandas as pd

def make_bchart(df, year=2024, top_n=16):
    prueba_admision = "PSU"
    nombres_pruebas = {
    "MATE1_REG_ACTUAL": "Competencia Matemática 1",
    "MATE2_REG_ACTUAL": "Competencia Matemática 2",
    "CLEC_REG_ACTUAL": "Competencia Lectora",
    "CIEN_REG_ACTUAL": "Ciencias",
    "HCSOC_REG_ACTUAL": "Historia y Ciencias Sociales",

    "MATE_ACTUAL": "Matemáticas",
    "LENG_ACTUAL": "Lenguaje",
    "CIEN_ACTUAL": "Ciencias",
    "HCSO_ACTUAL": "Historia y Ciencias Sociales"
    }
    if year>=2024:
        pruebas = ["MATE1_REG_ACTUAL", "MATE2_REG_ACTUAL", "HCSOC_REG_ACTUAL", "CIEN_REG_ACTUAL", "CLEC_REG_ACTUAL"]
        prueba_admision="PAES"
    else:
        pruebas = ["MATE_ACTUAL", "HCSO_ACTUAL", "CIEN_ACTUAL", "LENG_ACTUAL"]
    df= df.melt(
        id_vars=["COD_REG_RBD", "CONEXIONES_POR_VIVIENDA", "POP", "REGION_NOMBRE"],
        value_vars=pruebas,
        var_name="TIPO_PRUEBA",
        value_name="PUNTAJE"
    )

    df["TIPO_PRUEBA"] = df["TIPO_PRUEBA"].map(nombres_pruebas)
    fig = aux_make_bchart(df, top_n, prueba_admision)
    return fig


def aux_make_bchart(df, top_n, prueba_admision):

    colors = {'Competencia Matemática 1':"rgb(255, 144, 14)",
               'Competencia Matemática 2':"rgb(132, 90, 204)",
                'Competencia Lectora':"rgb(50, 155, 170)",
                'Ciencias':"rgb(44, 160, 101)",
                'Historia y Ciencias Sociales':"rgb(168, 84, 50)",
                
                'Matemáticas':"rgb(255, 144, 14)",
                'Lenguaje':"rgb(50, 155, 170)",
                'Ciencias':"rgb(44, 160, 101)",
                'Historia y Ciencias Sociales':"rgb(168, 84, 50)"
            }
    fig = px.bar(
        df,
        x="PUNTAJE",
        y="REGION_NOMBRE",
        color="TIPO_PRUEBA",
        color_discrete_map=colors,
        title="Puntajes "+prueba_admision+" promedio por región y tipo de prueba",
        labels={"TIPO_PRUEBA": "Prueba", "REGION_NOMBRE": "Región", "PUNTAJE": "Puntaje"},
        orientation="h",
        
    )
    fig.update_layout(
        yaxis=dict(title="Región"),
        xaxis={"range":[1, 3500]}
    )
    return fig