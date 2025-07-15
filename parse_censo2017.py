import pandas as pd
df = pd.read_csv("Dataset\\Microdato_Censo2017-Viviendas.csv", sep=';', encoding='latin1')
df_filtrado = df.groupby('REGION', as_index=False)['CANT_HOG'].sum()
df_filtrado = df_filtrado.rename(columns={"REGION": "COD_REG_RBD"})
df_filtrado = df_filtrado.rename(columns={"CANT_HOG": "VIVIENDAS"})
df_filtrado.to_csv("Dataset\\Censo2017-Viviendas-Filtrado.csv")
