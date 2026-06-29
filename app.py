import mysql.connector
import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io

# =========================
# CONFIGURACIÓN
# =========================
st.set_page_config(page_title="Dashboard Big Data", layout="wide")

st.title("📊 Dashboard Estilo Power BI - Big Data")

# =========================
# CONEXIÓN MYSQL
# =========================
#conexion = mysql.connector.connect(
#    host="localhost",
#    user="root",
#    password="vivi.2006",
#    database="bd_lavadora"
#)

#df_base = pd.read_sql("SELECT * FROM cliente", con=conexion)

df = pd.read_csv("datos_practica.csv")

# Convertir Edad a número y eliminar filas con Edad vacía o None
df["Edad"] = pd.to_numeric(df["Edad"], errors="coerce")
df = df.dropna(subset=["Edad"])

# Convertir Salario a numérico
df["Salario"] = pd.to_numeric(df["Salario"], errors="coerce")

# Eliminar filas con nulos en Edad, Salario y Ciudad
df = df.dropna(subset=["Edad", "Salario", "Ciudad"])
# =========================
# MENÚ LATERAL (POWER BI STYLE)
# =========================
menu = st.sidebar.selectbox(
    "📌 Menú de Navegación",
    [
        "📂 Exploración de Datos",
        "🧹 Limpieza de Datos",
        "🔄 Transformación de Datos",
        "📊 Visualización",
        "📦 Dataset Final",
        "⬇️ Exportar Datos"
    ]
)

# =========================================================
# 📂 EXPLORACIÓN DE DATOS
# =========================================================
if menu == "📂 Exploración de Datos":

    st.header("Exploración de Datos")

    st.dataframe(df)

    st.subheader("Primeras filas")
    st.dataframe(df.head())

    st.subheader("Últimas filas")
    st.dataframe(df.tail())

    st.subheader("Info del DataFrame")

    buffer = io.StringIO()
    df.info(buf=buffer)
    st.text(buffer.getvalue())

    st.subheader("Estadísticas")
    st.dataframe(df.describe())

    st.subheader("Valores nulos")
    st.write(df.isnull().sum())

    st.subheader("Duplicados")
    st.write(df.duplicated().sum())

    st.subheader("Tipos de datos")
    st.dataframe(df.dtypes)

# =========================================================
# 🧹 LIMPIEZA DE DATOS
# =========================================================
elif menu == "🧹 Limpieza de Datos":

    st.header("Limpieza de Datos")

    # Convertir columnas numéricas
    st.subheader("Transformar valores a numéricos")
    df["Edad"] = pd.to_numeric(df["Edad"], errors="coerce")
    df["Salario"] = pd.to_numeric(df["Salario"], errors="coerce")

    # Contar valores nulos
    st.subheader("Contar valores nulos")
    st.write(df.isnull().sum())

    # Mostrar registros con Edad nula
    st.subheader("Registros con Edad nula")
    st.dataframe(df[df["Edad"].isnull()])

    # Reemplazar Edad con la media
    st.subheader("Reemplazar Edad nula con la media")
    df["Edad"] = df["Edad"].fillna(df["Edad"].mean())

    # Eliminar filas donde Salario sea nulo
    df = df.dropna(subset=["Salario"])

    # Eliminar filas donde Ciudad sea nula
    df = df.dropna(subset=["Ciudad"])
    st.write(df.loc[df["ID"] == 16])
    st.write(df.loc[df["ID"] == 11])
    # Eliminar duplicados
    st.subheader("Eliminar duplicados")
    df = df.drop_duplicates()

    # Mostrar resultado final
    st.subheader("Datos después de la limpieza")
    st.dataframe(df)

# =========================================================
# 🔄 TRANSFORMACIÓN DE DATOS
# =========================================================
elif menu == "🔄 Transformación de Datos":

    st.header("Transformación de Datos")

    # ------------------------
    # variable simulada ventas
    # ------------------------
    np.random.seed(42)
    df["ventas"] = np.random.randint(100, 1000, len(df))

    st.subheader("Dataset con ventas")
    st.dataframe(df)

    # ------------------------
    # Normalización
    # ------------------------
    df["ventas_norm"] = (
        (df["ventas"] - df["ventas"].min()) /
        (df["ventas"].max() - df["ventas"].min())
    )

    # ------------------------
    # Z-score
    # ------------------------
    df["ventas_z"] = (
        (df["ventas"] - df["ventas"].mean()) / df["ventas"].std()
    )

    # ------------------------
    # Log
    # ------------------------
    df["ventas_log"] = np.log1p(df["ventas"])
    
    # ------------------------
    # Binning
    # ------------------------
    df["categoria"] = pd.cut(
        df["ventas"],
        bins=[0, 300, 600, 1000],
        labels=["Bajo", "Medio", "Alto"]
    )

    st.subheader("Datos transformados")
    st.dataframe(df)
   # Aplicar transformación en la columna Edad
    df["categoria_edad"] = pd.cut(
    df["Edad"],
    bins=[0, 6, 12, 20, 25, 60, np.inf],
    labels=["Infancia", "Niñez", "Adolescencia", "Juventud", "Adultez", "Ancianidad"],
    include_lowest=True
    )

    # Eliminar filas donde la categoría quedó vacía (None)
    df = df.dropna(subset=["categoria_edad"])

    st.subheader("Datos transformados por categorías de edad")
    st.dataframe(df)
# =========================================================
# 📊 VISUALIZACIÓN (DASHBOARD POWER BI STYLE)
# =========================================================
elif menu == "📊 Visualización":

    st.header("Visualización de Datos")

    np.random.seed(42)
    df["ventas"] = np.random.randint(100, 1000, len(df))

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Distribución")
        fig, ax = plt.subplots()
        ax.hist(df["ventas"], bins=10)
        st.pyplot(fig)

    with col2:
        st.subheader("Outliers")
        fig, ax = plt.subplots()
        sns.boxplot(x=df["ventas"], ax=ax)
        st.pyplot(fig)

    st.subheader("Relación de datos")
    st.dataframe(df[["ventas"]])

# =========================================================
# 📦 DATASET FINAL
# =========================================================
elif menu == "📦 Dataset Final":

    st.header("Dataset Final Procesado")

    np.random.seed(42)
    df["ventas"] = np.random.randint(100, 1000, len(df))

    df["ventas_norm"] = (
        (df["ventas"] - df["ventas"].min()) /
        (df["ventas"].max() - df["ventas"].min())
    )

    df["ventas_z"] = (
        (df["ventas"] - df["ventas"].mean()) / df["ventas"].std()
    )

    df["ventas_log"] = np.log1p(df["ventas"])

    df["categoria"] = pd.cut(
        df["ventas"],
        bins=[0, 300, 600, 1000],
        labels=["Bajo", "Medio", "Alto"]
    )

    st.dataframe(df)

    st.subheader("Estadísticas finales")
    st.dataframe(df.describe())

# =========================================================
# ⬇️ EXPORTAR DATOS
# =========================================================
elif menu == "⬇️ Exportar Datos":

    st.header("Descarga de Datos Limpios")

    np.random.seed(42)
    df["ventas"] = np.random.randint(100, 1000, len(df))

    df["ventas_norm"] = (
        (df["ventas"] - df["ventas"].min()) /
        (df["ventas"].max() - df["ventas"].min())
    )

    df["ventas_z"] = (
        (df["ventas"] - df["ventas"].mean()) / df["ventas"].std()
    )

    df["ventas_log"] = np.log1p(df["ventas"])

    df["categoria"] = pd.cut(
        df["ventas"],
        bins=[0, 300, 600, 1000],
        labels=["Bajo", "Medio", "Alto"]
    )

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇️ Descargar CSV",
        data=csv,
        file_name="datos_transformados.csv",
        mime="text/csv"
    )