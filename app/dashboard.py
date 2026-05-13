
# IMPORTS

import sys
import os

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

sys.path.insert(0, BASE_DIR)

import streamlit as st
import pandas as pd
import plotly.express as px

from src.preproces import procesar_datos
from src.risk_model import RiskModel
from src.analysis import rendimiento_por_facultad

from src.auth import login

from src.load_data import (
    guardar_resultados,
    conectar_db,
    cargar_resultados,
    cargar_datos
)


# CONFIGURACIÓN PÁGINA

st.set_page_config(
    page_title="Dashboard Académico BI",
    layout="wide"
)

st.title(" Dashboard Académico BI")


# SESSION STATE

if "login" not in st.session_state:
    st.session_state.login = False

if "rol" not in st.session_state:
    st.session_state.rol = None

if "df" not in st.session_state:
    st.session_state.df = None

if "analizado" not in st.session_state:
    st.session_state.analizado = False


# LOGIN

if not st.session_state.login:

    st.title(" Iniciar Sesión")

    usuario = st.text_input("Usuario")

    password = st.text_input(
        "Contraseña",
        type="password"
    )

    if st.button("Ingresar"):

        resultado = login(usuario, password)

        if resultado["autenticado"]:

            st.session_state.login = True
            st.session_state.rol = resultado["rol"]

            st.success(" Login exitoso")

            st.rerun()

        else:

            st.error(" Usuario o contraseña incorrectos")

    st.stop()


# SIDEBAR

st.sidebar.title(" Configuración")

st.sidebar.success(
    f"Rol: {st.session_state.rol}"
)

if st.sidebar.button("Cerrar sesión"):

    st.session_state.login = False
    st.session_state.rol = None
    st.session_state.df = None
    st.session_state.analizado = False

    st.rerun()


# FUNCIONES

def leer_archivo(archivo):

    if archivo.name.endswith(".csv"):

        try:

            df = pd.read_csv(
                archivo,
                encoding="utf-8"
            )

        except:

            df = pd.read_csv(
                archivo,
                encoding="latin-1"
            )

    elif archivo.name.endswith(".xlsx"):

        df = pd.read_excel(archivo)

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    return df


def normalizar_columnas(df):

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    mapa = {

        "id_estudiante": [
            "id_estudiante",
            "id",
            "codigo",
            "student_id"
        ],

        "nota": [
            "nota",
            "calificacion",
            "score",
            "nota_final"
        ],

        "asistencia": [
            "asistencia",
            "attendance",
            "porcentaje"
        ],

        "facultad": [
            "facultad",
            "faculty",
            "carrera"
        ]
    }

    for destino, opciones in mapa.items():

        for col in df.columns:

            if col in opciones:

                df.rename(
                    columns={col: destino},
                    inplace=True
                )

    return df


# FILTROS

def aplicar_filtros(df):

    st.sidebar.subheader(" Filtros")

    df_filtrado = df.copy()

    # FACULTAD

    if "facultad" in df_filtrado.columns:

        facultades = ["Todas"] + list(
            df_filtrado["facultad"]
            .dropna()
            .unique()
        )

        facultad = st.sidebar.selectbox(
            "Filtrar Facultad",
            facultades
        )

        if facultad != "Todas":

            df_filtrado = df_filtrado[
                df_filtrado["facultad"] == facultad
            ]

    # RIESGO

    if "riesgo" in df_filtrado.columns:

        riesgos = ["Todos"] + list(
            df_filtrado["riesgo"]
            .dropna()
            .unique()
        )

        riesgo = st.sidebar.selectbox(
            "Filtrar Riesgo",
            riesgos
        )

        if riesgo != "Todos":

            df_filtrado = df_filtrado[
                df_filtrado["riesgo"] == riesgo
            ]

    # NOTA MÍNIMA

    if "promedio" in df_filtrado.columns:

        nota_min = st.sidebar.slider(
            "Nota mínima",
            0.0,
            5.0,
            0.0
        )

        df_filtrado = df_filtrado[
            df_filtrado["promedio"] >= nota_min
        ]

    return df_filtrado


# DOCENTE

if st.session_state.rol == "docente":

    st.subheader(" Visualización de resultados")

    st.info(
        "El docente solo puede visualizar resultados."
    )

    host = st.text_input(
        "Host",
        value="localhost",
        key="docente_host"
    )

    puerto = st.text_input(
        "Puerto",
        value="5432",
        key="docente_puerto"
    )

    usuario_bd = st.text_input(
        "Usuario BD",
        key="docente_usuario"
    )

    password_bd = st.text_input(
        "Contraseña BD",
        type="password",
        key="docente_password"
    )

    database = st.text_input(
        "Base de Datos",
        key="docente_database"
    )

    if st.button(" Ver resultados"):

        try:

            engine = conectar_db(
                host,
                puerto,
                usuario_bd,
                password_bd,
                database
            )

            df = cargar_resultados(engine)

            st.session_state.df = df
            st.session_state.analizado = True

            st.success(" Datos cargados correctamente")

        except Exception as e:

            st.error(f" Error: {e}")


# ADMIN

if st.session_state.rol == "admin":

    opcion = st.sidebar.selectbox(
        "Fuente de datos",
        ["CSV", "Base de Datos"]
    )

    
    # CSV
   

    if opcion == "CSV":

        st.subheader(" Subir archivos")

        archivo_notas = st.file_uploader(
            "Subir archivo de notas",
            type=["csv", "xlsx"]
        )

        archivo_asistencia = st.file_uploader(
            "Subir archivo de asistencia",
            type=["csv", "xlsx"]
        )

        archivo_estudiantes = st.file_uploader(
            "Subir archivo de estudiantes",
            type=["csv", "xlsx"]
        )

        guardar_bd = st.checkbox(
            "Guardar resultados en Base de Datos"
        )

        # CONFIG BD SOLO SI SE NECESITA

        if guardar_bd:

            st.subheader(" Configuración Base de Datos")

            host = st.text_input(
                "Host",
                value="localhost"
            )

            puerto = st.text_input(
                "Puerto",
                value="5432"
            )

            usuario_bd = st.text_input(
                "Usuario BD"
            )

            password_bd = st.text_input(
                "Contraseña BD",
                type="password"
            )

            database = st.text_input(
                "Base de Datos"
            )

        # ANALIZAR

        if st.button(" Analizar datos"):

            try:

                if not archivo_notas or not archivo_asistencia:

                    st.warning(
                        "Debes subir notas y asistencia"
                    )

                    st.stop()

                notas = normalizar_columnas(
                    leer_archivo(archivo_notas)
                )

                asistencia = normalizar_columnas(
                    leer_archivo(archivo_asistencia)
                )

                if archivo_estudiantes:

                    estudiantes = normalizar_columnas(
                        leer_archivo(archivo_estudiantes)
                    )

                else:

                    estudiantes = notas[
                        ["id_estudiante"]
                    ].drop_duplicates()

                    estudiantes["facultad"] = "General"

                # VALIDACIONES

                if "id_estudiante" not in notas.columns:

                    st.error(
                        " No existe id_estudiante en notas"
                    )

                    st.stop()

                if "nota" not in notas.columns:

                    st.error(
                        " No existe columna nota"
                    )

                    st.stop()

                if "id_estudiante" not in asistencia.columns:

                    st.error(
                        " No existe id_estudiante en asistencia"
                    )

                    st.stop()

                if "asistencia" not in asistencia.columns:

                    st.error(
                        " No existe columna asistencia"
                    )

                    st.stop()

                # PROCESAMIENTO

                df = procesar_datos(
                    estudiantes,
                    notas,
                    asistencia
                )

                modelo = RiskModel(df)

                df = modelo.aplicar_clasificacion()

                # GUARDAR EN SESSION

                st.session_state.df = df
                st.session_state.analizado = True

                # GUARDAR EN BD OPCIONAL

                if guardar_bd:

                    engine = conectar_db(
                        host,
                        puerto,
                        usuario_bd,
                        password_bd,
                        database
                    )

                    guardar_resultados(df, engine)

                    st.success(
                        " Datos analizados y guardados en BD"
                    )

                else:

                    st.success(
                        " Datos analizados correctamente"
                    )

            except Exception as e:

                st.error(f" Error: {e}")

    # BASE DE DATOS

    elif opcion == "Base de Datos":

        st.subheader(" Configuración Base de Datos")

        host = st.text_input(
            "Host",
            value="localhost"
        )

        puerto = st.text_input(
            "Puerto",
            value="5432"
        )

        usuario_bd = st.text_input(
            "Usuario BD"
        )

        password_bd = st.text_input(
            "Contraseña BD",
            type="password"
        )

        database = st.text_input(
            "Base de Datos"
        )

        if st.button("🔌 Conectar Base de Datos"):

            try:

                engine = conectar_db(
                    host,
                    puerto,
                    usuario_bd,
                    password_bd,
                    database
                )

                estudiantes, notas, asistencia = cargar_datos(
                    engine
                )

                df = procesar_datos(
                    estudiantes,
                    notas,
                    asistencia
                )

                modelo = RiskModel(df)

                df = modelo.aplicar_clasificacion()

                st.session_state.df = df
                st.session_state.analizado = True

                st.success(" Conexión exitosa")

            except Exception as e:

                st.error(f" Error BD: {e}")


# RESULTADOS

if st.session_state.analizado:

    df = st.session_state.df.copy()

    # FILTROS

    df = aplicar_filtros(df)

    st.subheader(" Datos procesados")

    st.dataframe(
        df,
        use_container_width=True
    )

    # KPIs

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            " Estudiantes",
            len(df)
        )

    with col2:

        st.metric(
            " Promedio",
            round(df["promedio"].mean(), 2)
        )

    with col3:

        st.metric(
            " Riesgo Alto",
            len(df[df["riesgo"] == "Alto"])
        )

    with col4:

        st.metric(
            " Asistencia",
            f"{round(df['asistencia'].mean(), 2)}%"
        )

    # PIE CHART

    st.subheader(" Distribución de riesgo")

    fig_riesgo = px.pie(
        df,
        names="riesgo"
    )

    st.plotly_chart(
        fig_riesgo,
        use_container_width=True
    )

    # FACULTADES

    st.subheader(" Rendimiento por facultad")

    facultades_df = rendimiento_por_facultad(df)

    fig_facultad = px.bar(
        facultades_df,
        x="facultad",
        y="promedio"
    )

    st.plotly_chart(
        fig_facultad,
        use_container_width=True
    )

    # DISPERSIÓN

    st.subheader(" Asistencia vs Promedio")

    fig_dispersion = px.scatter(
        df,
        x="asistencia",
        y="promedio",
        color="riesgo",
        hover_data=["id_estudiante"]
    )

    st.plotly_chart(
        fig_dispersion,
        use_container_width=True
    )

    # HISTOGRAMA

    st.subheader(" Distribución de notas")

    fig_hist = px.histogram(
        df,
        x="promedio",
        nbins=10
    )

    st.plotly_chart(
        fig_hist,
        use_container_width=True
    )

    # EXPORTAR

    archivo_exportado = "resultado_analisis.xlsx"

    df.to_excel(
        archivo_exportado,
        index=False
    )

    with open(archivo_exportado, "rb") as file:

        st.download_button(
            label=" Descargar Excel",
            data=file,
            file_name="resultado_analisis.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
