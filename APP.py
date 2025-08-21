import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder

st.set_page_config(page_title="EDA Deportes", layout="wide")
st.title("Análisis Exploratorio de Datos (EDA) - Deportes")

# Opciones para variables
var_cuant = ["Edad", "Puntaje", "Altura", "Peso", "Partidos", "Goles"]
var_cual = ["Deporte", "País", "Sexo", "Equipo", "Posición", "Categoría"]

# Selección de número de muestras y columnas
total_muestras = st.slider("Cantidad de muestras", min_value=50, max_value=500, value=100, step=10)
col_options = var_cuant + var_cual
cols_seleccionadas = st.multiselect("Selecciona hasta 6 columnas", col_options, default=col_options[:6], max_selections=6)

# Generación de datos sintéticos
def generar_datos(n, cols):
    data = {}
    deportes = ["Fútbol", "Baloncesto", "Tenis", "Natación", "Atletismo", "Voleibol"]
    paises = ["Colombia", "Brasil", "Argentina", "USA", "España", "Alemania"]
    sexos = ["M", "F"]
    equipos = ["A", "B", "C", "D", "E", "F"]
    posiciones = ["Delantero", "Defensa", "Portero", "Centrocampista", "Entrenador", "Suplente"]
    categorias = ["Profesional", "Amateur", "Juvenil", "Senior", "Master", "Infantil"]
    for col in cols:
        if col in var_cuant:
            if col == "Edad":
                data[col] = np.random.randint(15, 40, n)
            elif col == "Puntaje":
                data[col] = np.round(np.random.normal(50, 15, n), 2)
            elif col == "Altura":
                data[col] = np.round(np.random.normal(1.75, 0.15, n), 2)
            elif col == "Peso":
                data[col] = np.round(np.random.normal(70, 10, n), 1)
            elif col == "Partidos":
                data[col] = np.random.randint(1, 100, n)
            elif col == "Goles":
                data[col] = np.random.poisson(5, n)
        else:
            if col == "Deporte":
                data[col] = np.random.choice(deportes, n)
            elif col == "País":
                data[col] = np.random.choice(paises, n)
            elif col == "Sexo":
                data[col] = np.random.choice(sexos, n)
            elif col == "Equipo":
                data[col] = np.random.choice(equipos, n)
            elif col == "Posición":
                data[col] = np.random.choice(posiciones, n)
            elif col == "Categoría":
                data[col] = np.random.choice(categorias, n)
    return pd.DataFrame(data)

df = generar_datos(total_muestras, cols_seleccionadas)

st.subheader("Vista previa de la tabla de datos")
st.dataframe(df)

# Selección de tipo de gráfica
tipo_grafica = st.selectbox("Tipo de gráfica", ["Tendencia", "Barras", "Dispersión", "Pastel", "Histograma"])
col_grafica = st.selectbox("Columna para graficar", cols_seleccionadas)
col_grafica2 = st.selectbox("Columna secundaria (opcional)", ["Ninguna"] + cols_seleccionadas)

fig, ax = plt.subplots(figsize=(8, 5))
if tipo_grafica == "Tendencia":
    if col_grafica in var_cuant:
        ax.plot(df[col_grafica])
        ax.set_title(f"Tendencia de {col_grafica}")
        ax.set_xlabel("Índice")
        ax.set_ylabel(col_grafica)
    else:
        st.warning("Selecciona una variable cuantitativa para tendencia.")
elif tipo_grafica == "Barras":
    if col_grafica in var_cual:
        df[col_grafica].value_counts().plot.bar(ax=ax)
        ax.set_title(f"Barras de {col_grafica}")
        ax.set_ylabel("Frecuencia")
    elif col_grafica in var_cuant:
        if col_grafica2 != "Ninguna" and col_grafica2 in var_cual:
            df.groupby(col_grafica2)[col_grafica].mean().plot.bar(ax=ax)
            ax.set_title(f"Media de {col_grafica} por {col_grafica2}")
            ax.set_ylabel(f"Media de {col_grafica}")
        else:
            st.warning("Selecciona una columna secundaria cualitativa para barras de cuantitativas.")
elif tipo_grafica == "Dispersión":
    if col_grafica2 != "Ninguna" and col_grafica in var_cuant and col_grafica2 in var_cuant:
        ax.scatter(df[col_grafica], df[col_grafica2])
        ax.set_title(f"Dispersión: {col_grafica} vs {col_grafica2}")
        ax.set_xlabel(col_grafica)
        ax.set_ylabel(col_grafica2)
    else:
        st.warning("Selecciona dos variables cuantitativas para dispersión.")
elif tipo_grafica == "Pastel":
    if col_grafica in var_cual:
        df[col_grafica].value_counts().plot.pie(ax=ax, autopct='%1.1f%%')
        ax.set_title(f"Gráfico de pastel de {col_grafica}")
        ax.set_ylabel("")
    else:
        st.warning("Selecciona una variable cualitativa para pastel.")
elif tipo_grafica == "Histograma":
    if col_grafica in var_cuant:
        ax.hist(df[col_grafica], bins=20, color='skyblue', edgecolor='black')
        ax.set_title(f"Histograma de {col_grafica}")
        ax.set_xlabel(col_grafica)
        ax.set_ylabel("Frecuencia")
    else:
        st.warning("Selecciona una variable cuantitativa para histograma.")

st.pyplot(fig)

st.markdown("---")
st.write("Desarrollado por GitHub Copilot")
