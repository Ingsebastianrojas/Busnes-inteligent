import pandas as pd
from sqlalchemy import create_engine



# CONEXIÓN BD


def conectar_db(
    host,
    puerto,
    usuario,
    password,
    database
):

    url = (
        f"postgresql+psycopg2://{usuario}:{password}"
        f"@{host}:{puerto}/{database}"
    )

    engine = create_engine(url)

    return engine



#  CARGAR TABLAS


def cargar_datos(engine):

    estudiantes = pd.read_sql(
        "SELECT * FROM estudiantes",
        engine
    )

    notas = pd.read_sql(
        "SELECT * FROM notas",
        engine
    )

    asistencia = pd.read_sql(
        "SELECT * FROM asistencia",
        engine
    )

    return estudiantes, notas, asistencia



#  GUARDAR RESULTADOS


def guardar_resultados(df, engine):

    df.to_sql(
        "resultado_analisis",
        engine,
        if_exists="replace",
        index=False
    )


#  CARGAR RESULTADOS


def cargar_resultados(engine):

    query = "SELECT * FROM resultado_analisis"

    df = pd.read_sql(
        query,
        engine
    )

    return df