import pandas as pd
import plotly.express as px

def make_scatter_matricula_vs_gasto():
    # Cargar datos
    df = pd.read_csv("Dataset/TasaMatriculaGastoPublico.csv")

    # Crear scatter plot
    fig = px.scatter(
        df,
        x="TASA_MATRICULA",
        y="GASTO_EDUCACION_PER_CAPITA",
        text="AÑO",
        labels={
            "TASA_MATRICULA": "Tasa de matrícula promedio nacional (%)",
            "GASTO_EDUCACION_PER_CAPITA": "Gasto público en educación per cápita (CLP)"
        },
        title="Relación entre tasa de matrícula nacional y gasto público en educación per cápita"
    )

    # Estilo
    fig.update_traces(marker=dict(size=10, color="royalblue"), textposition="top center")
    fig.update_layout(
        width=700,
        height=400,
        title_x=0.5
    )

    return fig
