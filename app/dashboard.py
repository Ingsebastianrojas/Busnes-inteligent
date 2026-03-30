import streamlit as st
import sys
import os

from src.load_data import cargar_datos
from src.preproces import procesar_datos
from src.risk_model import RiskModel
from src.analysis import rendimiento_por_facultad, conteo_riesgo

sys.path.append(os.path.abspath(os.path.join(os.path.dirname("C:\\Users\\Sebas\\Documents\\Proyectos\\busnes inteligent\\src"), "..")))

st.title("Dashboard Académico BI")

# Cargar datos
estudiantes, notas, asistencia = cargar_datos()

# Procesar
df = procesar_datos(estudiantes, notas, asistencia)

# Modelo de riesgo
modelo = RiskModel(df)
df = modelo.aplicar_clasificacion()

# Mostrar tabla
st.subheader("Datos procesados")
st.dataframe(df)

# Análisis
st.subheader("Rendimiento por facultad")
facultades = rendimiento_por_facultad(df)
st.bar_chart(facultades.set_index("facultad"))

st.subheader("Distribución de riesgo")
riesgo = df["riesgo"].value_counts()
st.bar_chart(riesgo)


