import pandas as pd
year=2024
# para mapear el dataset de poblacion
regiones_list=[15, 1, 2, 3, 4, 5, 13, 6, 7, 16, 8, 9, 14, 10, 11, 12]
regiones = {
    "1.": None,
    "1.1.": 15,  # Región de Arica y Parinacota
    "1.2.": 1,   # Región de Tarapacá
    "1.3.": 2,   # Región de Antofagasta
    "1.4.": 3,   # Región de Atacama
    "1.5.": 4,   # Región de Coquimbo
    "1.6.": 5,   # Región de Valparaíso
    "1.7.": 13,  # Región Metropolitana de Santiago
    "1.8.": 6,   # Región del Libertador General Bernardo O’Higgins
    "1.9.": 7,   # Región del Maule
    "1.10.": 8,  # Región del Biobío
    "1.11.": 16, # Región de Ñuble
    "1.12.": 9,  # Región de La Araucanía
    "1.13.": 14, # Región de Los Ríos
    "1.14.": 10, # Región de Los Lagos
    "1.15.": 11, # Región de Aysén del General Carlos Ibáñez del Campo
    "1.16.": 12  # Región de Magallanes y la Antártica Chilena
}

#nose
regiones_romano = {
    "I": 1,
    "II": 2,
    "III": 3,
    "IV": 4,
    "V": 5,
    "VI": 6,
    "VII": 7,
    "VIII": 8,
    "IX": 9,
    "X": 10,
    "XI": 11,
    "XII": 12,
    "RM": 13,
    "XIV": 14,
    "XV": 15,
    "XVI": 16
}

regiones_romano_2002 = {
    "I": 1,
    "II": 2,
    "III": 3,
    "IV": 4,
    "V": 5,
    "VI": 6,
    "VII": 7,
    "VIII": 8,
    "IX": 9,
    "X": 10,
    "XI": 11,
    "XII": 12,
    "RM": 13,
}

def set_year(n):
    global year
    year = n

def limpiar_y_mapear_regiones(df, diccionario_regiones):
    df = df.copy()
    df["Descripción series"] = (
        df["Descripción series"]
        .astype(str)
        .str.replace("\xa0", "", regex=False)
        .str.strip()
    )
    df["Código Región"] = df["Descripción series"].map(diccionario_regiones)
    return df
def get_df_pop():
    df_pop = pd.read_excel("Dataset\\poblacion.xlsx", skiprows=2)
    col_year = pd.Timestamp(str(year)+"-01-01")
    df_pop["COD_REG_RBD"] = df_pop["Reg"].map((regiones))
    df_year_pop = df_pop[col_year]
    df_year_pop = df_pop[[col_year, "COD_REG_RBD"]]
    df_year_pop = df_year_pop.rename(columns={col_year: "POP"})
    return df_year_pop
def get_df_rendimiento():   
    df_rendimiento = pd.read_csv("Dataset\\rendimiento\\"+str(year)+".csv", sep=',', encoding='latin1', decimal='.')
    return df_rendimiento
def get_df_internet():
    if year != 2002:
        df_inter = pd.read_excel("Dataset\\CONEXIONES_INTERNET_FIJA.xlsx", sheet_name="7.4.Co_RG", skiprows=16)
    else:
        df_inter = pd.read_excel("Dataset\\CONEXIONES_INTERNET_FIJA.xlsx", sheet_name="7.4.Co_RG", skiprows=6, nrows=8)
    # el excel no tiene cada fila con un año asociado... 
    df_inter["Año"] = df_inter["Año"].ffill()
    df_inter_year = df_inter[(df_inter["Año"] == year) & (df_inter["Mes"] == "Dic")]
    if df_inter_year.empty:
        raise ValueError(f"No hay datos para el año {year}. oops")
    if year != 2002:
        df_conex = df_inter_year[list(regiones_romano.keys())].T
    else:
        df_conex = df_inter_year[list(regiones_romano_2002.keys())].T
    df_conex.reset_index(inplace=True)
    df_conex.columns = ["ROMANO", "NUM_CONEXIONES_FIJAS"]
    df_conex["COD_REG_RBD"] = df_conex["ROMANO"].map(regiones_romano)

    df_conex = df_conex[["COD_REG_RBD", "NUM_CONEXIONES_FIJAS"]]
    return df_conex

def get_df_viviendas():
    if year==2017:
        df_vivi = pd.read_csv("Dataset\\Censo2017-Viviendas-Filtrado.csv")
    else:
        df_vivi = pd.read_excel("Dataset\\CensosVivienda200220172024.xlsx", sheet_name="Total Viviendas", skiprows=5)
        df_vivi = df_vivi.drop(columns=["Comuna", "Código Comuna INE", "Viviendas Particulares", "Viviendas Colectivas", "Viviendas Particulares Ocupadas con Moradores Presentes"])

        df_vivi = pd.concat([
            df_vivi.iloc[3:19]
        ])
        # renames raros para arreglar el problema del doble header
        df_vivi = df_vivi.rename(columns={"Total Viviendas": "2002"})
        df_vivi = df_vivi.rename(columns={"Unnamed: 4": "2007"})
        df_vivi = df_vivi.rename(columns={"Unnamed: 5": "2024"})
        df_vivi = df_vivi.reset_index().rename(columns={'index': 'COD_REG_RBD'})
        df_vivi["COD_REG_RBD"]=regiones_list
        columnas_utiles = ["COD_REG_RBD", str(year)]
        df_vivi = df_vivi[columnas_utiles]
        df_vivi = df_vivi.reset_index().rename(columns={str(year): 'VIVIENDAS'})
        
    return df_vivi


def get_df_prueba():
    if year >= 2024:
        df_prueba = pd.read_csv("Dataset\\Promedio Admisión PAES\\PromedioPorRegion"+str(year)+".csv")
    elif year == 2023:
        df_prueba = pd.read_csv("Dataset\\Promedio Admisión 2023\\PromedioPorRegion"+str(year)+".csv")
    elif year==2021 or year==2022:
        df_prueba = pd.read_csv("Dataset\\Promedios Admisión PDT\\PromedioPorRegion"+str(year)+".csv")
    else:
        df_prueba = pd.read_csv("Dataset\\Promedios Admisión PSU\\PromedioPorRegion"+str(year)+".csv")
    df_prueba = df_prueba.rename(columns={"CODIGO_REGION": 'COD_REG_RBD'})
    return df_prueba


def get_df_pobreza():
    df = pd.read_excel("Dataset\\PLANILLA_Estimaciones_comunales_tasa_pobreza_por_ingresos_multidimensional_2017.xlsx", skiprows=2)
    print(df.columns.tolist())
    df['% pobreza'] = df['Porcentaje de personas en situación de pobreza por ingresos 2017']
    df_ordenado = df.sort_values('% pobreza')
    comunas_menos_pobreza = df_ordenado.head(20).reset_index(drop=True)
    comunas_mas_pobreza = df_ordenado.tail(20).sort_values('% pobreza', ascending=False).reset_index(drop=True)
    print("Menor pobreza:")
    print(comunas_menos_pobreza[['Nombre comuna', '% pobreza']])
    print("\nMayor pobreza:")
    print(comunas_mas_pobreza[['Nombre comuna', '% pobreza']])
    return comunas_mas_pobreza, comunas_menos_pobreza