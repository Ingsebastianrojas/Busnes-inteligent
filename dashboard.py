import sys
import os


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, BASE_DIR)

import streamlit as st
import pandas as pd

from src.preproces import procesar_datos  
from src.risk_model import RiskModel
from src.analysis import rendimiento_por_facultad



#  FUNCIONES 


def leer_archivo(archivo):
    if archivo.name.endswith(".csv"):
        try:
            df = pd.read_csv(archivo, encoding="utf-8")
        except:
            df = pd.read_csv(archivo, encoding="latin-1")
    elif archivo.name.endswith(".xlsx"):
        df = pd.read_excel(archivo)

    #  limpiar nombres de columnas
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    return df


def normalizar_columnas(df):
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    mapa = {
        "id_estudiante": ["id_estudiante", "id", "codigo", "estudiante", "student_id"],
        "nota": ["nota", "calificacion", "score", "nota_final"],
        "asistencia": ["asistencia", "attendance", "porcentaje", "asistencia_%"]
    }

    for destino, opciones in mapa.items():
        for col in df.columns:
            if col in opciones:
                df.rename(columns={col: destino}, inplace=True)

    return df






st.title(" Dashboard Académico BI")

opcion = st.selectbox(
    "Selecciona fuente de datos",
    ["CSV", "Base de Datos"]
)



#  OPCIÓN CSV

if opcion == "CSV":

    st.subheader(" Subir archivos")

    archivo_notas = st.file_uploader("Subir notas", type=["csv", "xlsx"])
    archivo_asistencia = st.file_uploader("Subir asistencia", type=["csv", "xlsx"])
    archivo_estudiantes = st.file_uploader("Subir estudiantes (opcional)", type=["csv", "xlsx"])

    #  BOTÓN DE EJECUCIÓN
    if st.button(" Analizar datos"):

        if not archivo_notas or not archivo_asistencia:
            st.warning(" Debes subir al menos notas y asistencia")
            st.stop()

        try:
            #  Leer + normalizar
            notas = normalizar_columnas(leer_archivo(archivo_notas))
            asistencia = normalizar_columnas(leer_archivo(archivo_asistencia))

            if archivo_estudiantes:
                estudiantes = normalizar_columnas(leer_archivo(archivo_estudiantes))
            else:
                estudiantes = notas[["id_estudiante"]].drop_duplicates()
                estudiantes["facultad"] = "General"

            #  DEBUG (puedes quitar luego)
            st.write("Columnas notas:", notas.columns)
            st.write("Columnas asistencia:", asistencia.columns)

            #  VALIDACIONES FLEXIBLES
            if "id_estudiante" not in notas.columns:
                st.error(f"❌ Columnas encontradas en notas: {list(notas.columns)}")
                st.error("No se encontró identificador de estudiante")
                st.stop()

            if "nota" not in notas.columns:
                st.error("❌ El archivo de notas debe tener columna de nota")
                st.stop()

            if "id_estudiante" not in asistencia.columns:
                st.error("❌ El archivo de asistencia no tiene identificador")
                st.stop()

            if "asistencia" not in asistencia.columns:
                st.error("❌ El archivo de asistencia debe tener columna asistencia")
                st.stop()

            #  Procesar
            df = procesar_datos(estudiantes, notas, asistencia)

            #  Modelo de riesgo
            modelo = RiskModel(df)
            df = modelo.aplicar_clasificacion()

            #  RESULTADOS
            st.success(" Análisis completado")

            st.subheader(" Datos procesados")
            st.dataframe(df)

            #  KPI
            st.metric("Estudiantes en riesgo alto", len(df[df["riesgo"] == "Alto"]))

            # Gráficas
            st.subheader(" Distribución de riesgo")
            st.bar_chart(df["riesgo"].value_counts())

            st.subheader(" Rendimiento por facultad")
            facultades = rendimiento_por_facultad(df)
            st.bar_chart(facultades.set_index("facultad"))

        except Exception as e:
            st.error(f"❌ Error: {e}")



#  OPCIÓN BASE DE DATOS


elif opcion == "Base de Datos":

    if st.button("Conectar a la base de datos"):

        try:
            from src.load_data import cargar_datos

            estudiantes, notas, asistencia = cargar_datos()

            df = procesar_datos(estudiantes, notas, asistencia)

            modelo = RiskModel(df)
            df = modelo.aplicar_clasificacion()

            st.dataframe(df)

        except Exception as e:
            st.error(f"❌ Error BD: {e}")