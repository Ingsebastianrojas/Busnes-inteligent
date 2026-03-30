def estudiantes_en_riesgo(df):
    return df[df["riesgo"] == "Alto"]

def rendimiento_por_facultad(df):
    return df.groupby("facultad")["promedio"].mean().reset_index()

def conteo_riesgo(df):
    return df["riesgo"].value_counts().reset_index()