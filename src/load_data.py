import pandas as pd
from sqlalchemy import create_engine


def conectar_db():
    engine = create_engine("postgresql://Posgres:Pg123456@localhost/promedios")  # puedes cambiar a PostgreSQL
    return engine

def cargar_estudiantesbd(engine):
    return pd.read_sql("SELECT * FROM estudiantes", engine)

def cargar_estudiantes():
    return pd.read_csv("data/estudiantes.csv")

def cargar_notas_csv():
    return pd.read_csv("data/notas.csv")

def cargar_asistencia_csv():
    return pd.read_csv("data/asistencia.csv")

def cargar_datos():
    engine = conectar_db()
    estudiantes = cargar_estudiantes(engine)
    notas = cargar_notas_csv()
    asistencia = cargar_asistencia_csv()
    
    return estudiantes, notas, asistencia