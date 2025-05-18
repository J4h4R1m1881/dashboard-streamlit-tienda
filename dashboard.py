
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración general
sns.set_style("whitegrid")
st.set_page_config(page_title="Dashboard de Ventas", layout="wide")

# Cargar datos
df = pd.read_csv("data.csv")
df['Date'] = pd.to_datetime(df['Date'])

# Sidebar para seleccionar análisis
analisis = st.sidebar.selectbox(
    "Selecciona un análisis",
    [
        "Evolución de Ventas Totales",
        "Ingresos por Línea de Producto",
        "Distribución del Rating",
        "Total por Tipo de Cliente",
        "Método de Pago",
        "Costo vs Ganancia Bruta",
        "Correlación Numérica",
        "Ingreso Bruto por Sucursal y Línea"
    ]
)

# Análisis 1
if analisis == "Evolución de Ventas Totales":
    datos = df.groupby('Date')['Total'].sum().reset_index()
    fig, ax = plt.subplots()
    sns.lineplot(data=datos, x='Date', y='Total', marker='o', ax=ax)
    ax.set_title("Evolución de las Ventas Totales")
    st.pyplot(fig)

# Análisis 2
elif analisis == "Ingresos por Línea de Producto":
    resumen = df.groupby('Product line')['Total'].sum().sort_values(ascending=False).reset_index()
    fig, ax = plt.subplots()
    sns.barplot(data=resumen, x='Total', y='Product line', palette='viridis', ax=ax)
    ax.set_title("Ingresos por Línea de Producto")
    st.pyplot(fig)

# Análisis 3
elif analisis == "Distribución del Rating":
    fig, axs = plt.subplots(1, 2, figsize=(12, 5))
    sns.histplot(df['Rating'], bins=10, kde=True, ax=axs[0])
    axs[0].set_title("Distribución del Rating")
    sns.boxplot(x=df['Rating'], ax=axs[1])
    axs[1].set_title("Boxplot del Rating")
    st.pyplot(fig)

# Análisis 4
elif analisis == "Total por Tipo de Cliente":
    fig, ax = plt.subplots()
    sns.boxplot(data=df, x='Customer type', y='Total', palette='pastel', ax=ax)
    ax.set_title("Total por Tipo de Cliente")
    st.pyplot(fig)

# Análisis 5
elif analisis == "Método de Pago":
    pagos = df['Payment'].value_counts().reset_index()
    pagos.columns = ['Método de Pago', 'Cantidad']
    fig, ax = plt.subplots()
    sns.barplot(data=pagos, x='Cantidad', y='Método de Pago', palette='Set2', ax=ax)
    ax.set_title("Método de Pago más Utilizado")
    st.pyplot(fig)

# Análisis 6
elif analisis == "Costo vs Ganancia Bruta":
    fig, ax = plt.subplots()
    sns.scatterplot(data=df, x='cogs', y='gross income', hue='Branch', alpha=0.7, ax=ax)
    ax.set_title("Relación entre Costo y Ganancia Bruta")
    st.pyplot(fig)

# Análisis 7
elif analisis == "Correlación Numérica":
    columnas = ['Unit price', 'Quantity', 'Tax 5%', 'Total', 'cogs', 'gross income', 'Rating']
    corr = df[columnas].corr()
    fig, ax = plt.subplots(figsize=(10, 7))
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
    ax.set_title("Correlación entre Variables Numéricas")
    st.pyplot(fig)

# Análisis 8
elif analisis == "Ingreso Bruto por Sucursal y Línea":
    resumen = df.groupby(['Branch', 'Product line'])['gross income'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=resumen, x='Branch', y='gross income', hue='Product line', ax=ax)
    ax.set_title("Ingreso Bruto por Sucursal y Línea de Producto")
    st.pyplot(fig)
