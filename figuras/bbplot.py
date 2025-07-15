import plotly.express as px
def make_bbplot(df, nombre_prueba, color="M1"):
    # ASI ES, MATEMATICAS ES AMARILLO Y LENGUAJE ES AZUL
    colors = {"M1": "rgb(255, 144, 14)", "M2": "rgb(132, 90, 204)", "LENGUAJE":"rgb(255, 144, 14)",
               "CIENCIAS":"rgb(44, 160, 101)", "HISTORIA":"rgb(168, 84, 50)"}
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
        yaxis=dict(title="Promedio académico promedio", range=[1,1000])
    )
    return fig