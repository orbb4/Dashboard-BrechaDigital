import pandas as pd

for year in range(2002, 2025):
    # tuve que renombrar una carpeta y varios csv porque no seguian el estandar de nombramiento(?)
    df = pd.read_csv("Dataset\\rendimiento_original\\Rendimiento-"+str(year)+"\\Rendimiento por estudiante "+str(year)+".csv", sep=';', encoding='latin1', decimal=',')
    #df["PROM_GRAL"] = df["PROM_GRAL"].replace(",", ".")
    try:
        df["PROM_GRAL"] = pd.to_numeric(df["PROM_GRAL"])
    except:
        df["prom_gral"] = pd.to_numeric(df["prom_gral"])
    try:
        df_filtered = df.groupby(["COD_REG_RBD"]).agg({
            "PROM_GRAL": "mean",
            "MRUN": "count" # cantidad de alumnos
        }).reset_index().rename(columns={"MRUN": "n_estudiantes"})
    # por algun motivo en 2012 cambiaron el formato de los datos
    except:
        df_filtered = df.groupby(["cod_reg_rbd"]).agg({
            "prom_gral": "mean",
            "mrun": "count" # cantidad de alumnos
        }).reset_index().rename(columns={"mrun": "n_estudiantes"})
    print(year)
    print(df_filtered)
    df_filtered.to_csv("Dataset/rendimiento/"+str(year)+".csv", index=False, encoding="utf-8")