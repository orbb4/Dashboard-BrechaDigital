import plotly.express as px
def make_bbplot(df):
    fig = px.scatter(
        df,
        x="CONEXIONES_POR_VIVIENDA",
        y="PROM_GRAL",
        size_max=65,
        hover_name="COD_REG_RBD",
        size="POP",
    )
    fig.update_layout(
        dragmode='zoom',
        xaxis=dict(title="Conexiones fijas a internet por habitante (%)", range=[0, 100], tickformat=".0f"),
        yaxis=dict(title="Promedio académico promedio", range=[1,7])
    )
    return fig