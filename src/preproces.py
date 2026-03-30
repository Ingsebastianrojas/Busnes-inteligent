import pandas as pd

def procesar_datos(estudiantes, notas, asistencia):
    # Promedio por estudiante
    promedio = notas.groupby("id_estudiante")["nota"].mean().reset_index()
    promedio.rename(columns={"nota": "promedio"}, inplace=True)

    # Unir datos
    df = estudiantes.merge(promedio, on="id_estudiante")
    df = df.merge(asistencia, on="id_estudiante")

    return df