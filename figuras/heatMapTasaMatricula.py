import pandas as pd
import plotly.graph_objects as go

def make_heatmapMatriculas():
    # cargar archivos y agregar coolumna año, que no tienen
    df_2007 = pd.read_csv("Dataset/TasaMatriculaConexiones/datos_combinados2007.csv")
    df_2007["Año"] = 2007

    df_2017 = pd.read_csv("Dataset/TasaMatriculaConexiones/datos_combinados2017.csv")
    df_2017["Año"] = 2017

    df_2024 = pd.read_csv("Dataset/TasaMatriculaConexiones/datos_combinados2024.csv")
    df_2024["Año"] = 2024

    # unir los archivos
    df = pd.concat([df_2007, df_2017, df_2024], ignore_index=True)
    df["Año"] = df["Año"].astype(str)

    # definir parámetros del heatmap filas = regiones, columnas = años, valores = porcentaje de conexiones por vivienda
    matriz = df.pivot(index='NOMBRE_REGION', columns='Año', values='TASA_MATRICULA')

    # Crear matriz para conexiones por vivienda, misma estructura
    conexiones = df.pivot(index='NOMBRE_REGION', columns='Año', values='CONEXIONES_POR_VIVIENDA')
    admisiones = df.pivot(index='NOMBRE_REGION', columns='Año', values='NUM_ESTUDIANTES_ADMISION')
    matriculas = df.pivot(index='NOMBRE_REGION', columns='Año', values='NUM_ESTUDIANTES_MATRICULADOS')

   # texto de la etiqueta
    hovertext = []
    for region in matriz.index:
        fila = []
        for año in matriz.columns:
            tasa_matricula = matriz.loc[region, año]
            tasa_conexiones = conexiones.loc[region, año]
            num_admisiones = admisiones.loc[region, año]
            num_matriculas = matriculas.loc[region, año]
            tasa_text = f"{tasa_matricula:.2f}" if not pd.isna(tasa_matricula) else "Sin dato"
            conexiones_text = f"{tasa_conexiones:.2f}" if not pd.isna(tasa_conexiones) else "Sin dato"
            admisiones_text = f"{int(num_admisiones)}" if not pd.isna(num_admisiones) else "Sin dato"
            matriculas_text = f"{int(num_matriculas)}" if not pd.isna(num_matriculas) else "Sin dato"
            fila.append(
                f"<b>Región:</b> {region}<br>"
                f"<b>Año:</b> {año}<br>"
                f"<b>Tasa de matrícula:</b> {tasa_text}%<br>"
                f"<b>Conexiones fijas a internet por vivienda:</b> {conexiones_text}%<br>"
                f"<b>Total de estudiantes que rindieron la rdmisión:</b> {admisiones_text}<br>"
                f"<b>Total de estudiantes matriculados:</b> {matriculas_text}"
            )
        hovertext.append(fila)

    # crear el heatmap
    fig = go.Figure(data=go.Heatmap(
        z=matriz.values,
        x=matriz.columns,
        y=matriz.index,
        text=hovertext,
        hoverinfo='text',
        colorscale='Reds',
        colorbar=dict(title="Tasa de Matrículas (%)")
    ))

    fig.update_layout(
        width=500,
        height=600,
        #title="Tasa de ingreso a la educación superior por región y año",
        title={
        'text': "Tasa de ingreso a la educación superior por región y año",
        'font': dict(size=16),  
        'x': 0.5,
        'xanchor': 'center'
        },
        xaxis_title="Año",
        yaxis_title="Región"
    )

    return fig
