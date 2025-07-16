import plotly.express as px

def make_bbplot(df, nombre_prueba, color="M1", paes=True):
    # ASI ES, MATEMATICAS ES AMARILLO Y LENGUAJE ES AZUL
    colors = {"M1": "rgb(255, 144, 14)", "M2": "rgb(132, 90, 204)", "LENGUAJE":"rgb(50, 155, 170)",
               "CIENCIAS":"rgb(44, 160, 101)", "HISTORIA":"rgb(168, 84, 50)", "MATEMATICA": "rgb(255, 144, 14)"}
    yaxis_limit = 850
    if paes:
        yaxis_limit=1000
    fig = px.scatter(
        df,
        x="CONEXIONES_POR_VIVIENDA",
        y=nombre_prueba,
        size_max=65,
        hover_name="COD_REG_RBD",
        size="POP",
        color_discrete_sequence=[colors[color]]
    )
    fig.update_layout(
        dragmode='zoom',
        xaxis=dict(title="Conexiones fijas a internet por habitante (%)", range=[0, 100], tickformat=".0f"),
        yaxis=dict(title="Puntaje promedio", range=[1,yaxis_limit])
    )
    return fig