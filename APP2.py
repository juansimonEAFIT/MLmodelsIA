import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="EDA Dinámico Agricultura", layout="wide")
st.title("Análisis Exploratorio de Datos (EDA) - Agricultura")

st.markdown("""
**Carga tu archivo CSV de datos agrícolas para iniciar el análisis exploratorio.**
- El archivo debe tener encabezados en la primera fila.
- Se recomienda que los datos estén limpios, pero la app intentará manejar valores vacíos y errores.
""")

archivo = st.file_uploader("Selecciona tu archivo CSV", type=["csv"])

if archivo:
    df = pd.read_csv(archivo)
    df = df.replace('error', np.nan)
    df = df.apply(pd.to_numeric, errors='ignore')
    st.success("Datos cargados correctamente.")
    st.write("Vista previa de los datos:")
    st.dataframe(df.head(20))

    var_cual = df.select_dtypes(include=['object']).columns.tolist()
    var_cuant = df.select_dtypes(include=[np.number]).columns.tolist()

    st.write(f"Variables cuantitativas: {var_cuant}")
    st.write(f"Variables cualitativas: {var_cual}")

    total_muestras = st.slider("Cantidad de muestras", min_value=50, max_value=min(500, len(df)), value=min(100, len(df)), step=10)
    col_options = var_cuant + var_cual
    cols_seleccionadas = st.multiselect("Selecciona hasta 6 columnas", col_options, default=col_options[:6], max_selections=6)

    df_viz = df[cols_seleccionadas].head(total_muestras)
    st.subheader("Vista previa de la tabla seleccionada")
    st.dataframe(df_viz)

    if st.checkbox("Mostrar estadísticas descriptivas"):
        st.write(df_viz.describe(include='all'))

    tipo_grafica = st.selectbox("Tipo de gráfica", ["Tendencia", "Barras", "Dispersión", "Pastel", "Histograma"])
    col_grafica = st.selectbox("Columna para graficar", cols_seleccionadas)
    col_grafica2 = st.selectbox("Columna secundaria (opcional)", ["Ninguna"] + cols_seleccionadas)

    fig, ax = plt.subplots(figsize=(8, 5))
    if tipo_grafica == "Tendencia":
        if col_grafica in var_cuant:
            ax.plot(df_viz[col_grafica].dropna())
            ax.set_title(f"Tendencia de {col_grafica}")
            ax.set_xlabel("Índice")
            ax.set_ylabel(col_grafica)
        else:
            st.warning("Selecciona una variable cuantitativa para tendencia.")
    elif tipo_grafica == "Barras":
        if col_grafica in var_cual:
            df_viz[col_grafica].value_counts().plot.bar(ax=ax)
            ax.set_title(f"Barras de {col_grafica}")
            ax.set_ylabel("Frecuencia")
        elif col_grafica in var_cuant:
            if col_grafica2 != "Ninguna" and col_grafica2 in var_cual:
                df_viz.groupby(col_grafica2)[col_grafica].mean().plot.bar(ax=ax)
                ax.set_title(f"Media de {col_grafica} por {col_grafica2}")
                ax.set_ylabel(f"Media de {col_grafica}")
            else:
                st.warning("Selecciona una columna secundaria cualitativa para barras de cuantitativas.")
    elif tipo_grafica == "Dispersión":
        if col_grafica2 != "Ninguna" and col_grafica in var_cuant and col_grafica2 in var_cuant:
            ax.scatter(df_viz[col_grafica], df_viz[col_grafica2])
            ax.set_title(f"Dispersión: {col_grafica} vs {col_grafica2}")
            ax.set_xlabel(col_grafica)
            ax.set_ylabel(col_grafica2)
        else:
            st.warning("Selecciona dos variables cuantitativas para dispersión.")
    elif tipo_grafica == "Pastel":
        if col_grafica in var_cual:
            df_viz[col_grafica].value_counts().plot.pie(ax=ax, autopct='%1.1f%%')
            ax.set_title(f"Gráfico de pastel de {col_grafica}")
            ax.set_ylabel("")
        else:
            st.warning("Selecciona una variable cualitativa para pastel.")
    elif tipo_grafica == "Histograma":
        if col_grafica in var_cuant:
            ax.hist(df_viz[col_grafica].dropna(), bins=20, color='skyblue', edgecolor='black')
            ax.set_title(f"Histograma de {col_grafica}")
            ax.set_xlabel(col_grafica)
            ax.set_ylabel("Frecuencia")
        else:
            st.warning("Selecciona una variable cuantitativa para histograma.")

    st.pyplot(fig)
    st.markdown("---")
    st.write("Desarrollado por GitHub Copilot")
else:
    st.info("Por favor carga un archivo CSV para comenzar el análisis.")
