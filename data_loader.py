import pandas as pd
year = 2018
# para mapear el dataset de poblacion
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
    df_inter = pd.read_excel("Dataset\\CONEXIONES_INTERNET_FIJA.xlsx", sheet_name="7.4.Co_RG", skiprows=16)
    # el excel no tiene cada fila con un año asociado... 
    df_inter["Año"] = df_inter["Año"].ffill()
    df_inter_year = df_inter[(df_inter["Año"] == year) & (df_inter["Mes"] == "Dic")]
    df_conex = df_inter_year[list(regiones_romano.keys())].T

    df_conex.reset_index(inplace=True)
    df_conex.columns = ["ROMANO", "NUM_CONEXIONES_FIJAS"]
    df_conex["COD_REG_RBD"] = df_conex["ROMANO"].map(regiones_romano)

    df_conex = df_conex[["COD_REG_RBD", "NUM_CONEXIONES_FIJAS"]]
    return df_conex

