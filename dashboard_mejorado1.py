
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

# Mostrar datos
if st.sidebar.checkbox("Mostrar Base de datos"):
    st.dataframe(df)

# Título general
st.title("📊 Dashboard de Ventas - Análisis Exploratorio")

st.markdown("""
Este dashboard permite visualizar distintos análisis del comportamiento de ventas y clientes de una tienda.
Utiliza el menú lateral para seleccionar un análisis específico. También puedes filtrar por sucursal para ver resultados personalizados.
""")

# Filtro por sucursal
branches = df['Branch'].unique()
sucursal_seleccionada = st.sidebar.selectbox("Filtrar por sucursal", options=["Todas"] + list(branches))

if sucursal_seleccionada != "Todas":
    df = df[df['Branch'] == sucursal_seleccionada]

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
##########################################
# Filtros adicionales
st.sidebar.markdown("### Filtros adicionales")

# Filtro por línea de producto
lineas = df['Product line'].unique()
linea_seleccionada = st.sidebar.multiselect("Filtrar por línea de producto", options=lineas, default=lineas)

# Filtro por tipo de cliente
tipos_cliente = df['Customer type'].unique()
tipo_cliente_seleccionado = st.sidebar.multiselect("Filtrar por tipo de cliente", options=tipos_cliente, default=tipos_cliente)

# Filtro por método de pago
metodos_pago = df['Payment'].unique()
metodo_pago_seleccionado = st.sidebar.multiselect("Filtrar por método de pago", options=metodos_pago, default=metodos_pago)

# # Filtro por rango de fechas
# min_fecha = df['Date'].min()
# max_fecha = df['Date'].max()
# rango_fechas = st.sidebar.date_input("Filtrar por rango de fechas", [min_fecha, max_fecha], min_value=min_fecha, max_value=max_fecha)

# Aplicar filtros seleccionados
df = df[
    (df['Product line'].isin(linea_seleccionada)) &
    (df['Customer type'].isin(tipo_cliente_seleccionado)) &
    (df['Payment'].isin(metodo_pago_seleccionado)) 
    # (df['Date'] >= pd.to_datetime(rango_fechas[0])) &
    # (df['Date'] <= pd.to_datetime(rango_fechas[1]))
]

#####################################

# Análisis 1
if analisis == "Evolución de Ventas Totales":
    st.subheader("📈 Evolución de Ventas Totales")
    st.markdown("Este gráfico muestra cómo evolucionaron las ventas totales a lo largo del tiempo.")
    datos = df.groupby('Date')['Total'].sum().reset_index()
    fig, ax = plt.subplots()
    sns.lineplot(data=datos, x='Date', y='Total', marker='o', ax=ax)
    ax.set_title("Evolución de las Ventas Totales")
    st.pyplot(fig)

# Análisis 2
elif analisis == "Ingresos por Línea de Producto":
    st.subheader("📦 Ingresos por Línea de Producto")
    st.markdown("Compara las ventas totales generadas por cada línea de producto.")
    resumen = df.groupby('Product line')['Total'].sum().sort_values(ascending=False).reset_index()
    fig, ax = plt.subplots()
    sns.barplot(data=resumen, x='Total', y='Product line', palette='viridis', ax=ax)
    ax.set_title("Ingresos por Línea de Producto")
    st.pyplot(fig)

# Análisis 3
elif analisis == "Distribución del Rating":
    st.subheader("⭐ Distribución del Rating")
    st.markdown("Observa la distribución y tendencia general de las valoraciones entregadas por los clientes.")
    fig, axs = plt.subplots(1, 2, figsize=(12, 5))
    sns.histplot(df['Rating'], bins=10, kde=True, ax=axs[0])
    axs[0].set_title("Distribución del Rating")
    sns.boxplot(x=df['Rating'], ax=axs[1])
    axs[1].set_title("Boxplot del Rating")
    st.pyplot(fig)

# Análisis 4
elif analisis == "Total por Tipo de Cliente":
    st.subheader("👥 Total por Tipo de Cliente")
    st.markdown("Compara el comportamiento de compra entre clientes regulares y miembros.")
    fig, ax = plt.subplots()
    sns.boxplot(data=df, x='Customer type', y='Total', palette='pastel', ax=ax)
    ax.set_title("Total por Tipo de Cliente")
    st.pyplot(fig)

# Análisis 5
elif analisis == "Método de Pago":
    st.subheader("💳 Método de Pago más Utilizado")
    st.markdown("Distribución de los métodos de pago más comunes entre los clientes.")
    pagos = df['Payment'].value_counts().reset_index()
    pagos.columns = ['Método de Pago', 'Cantidad']
    fig, ax = plt.subplots()
    sns.barplot(data=pagos, x='Cantidad', y='Método de Pago', palette='Set2', ax=ax)
    ax.set_title("Método de Pago")
    st.pyplot(fig)

# Análisis 6
elif analisis == "Costo vs Ganancia Bruta":
    st.subheader("💰 Relación entre Costo y Ganancia Bruta")
    st.markdown("Visualiza la relación entre el costo de los bienes vendidos y el ingreso bruto generado.")
    fig, ax = plt.subplots()
    sns.scatterplot(data=df, x='cogs', y='gross income', hue='Branch', alpha=0.7, ax=ax)
    ax.set_title("Costo vs Ganancia Bruta")
    st.pyplot(fig)

# Análisis 7
elif analisis == "Correlación Numérica":
    st.subheader("🔢 Correlación entre Variables Numéricas")
    st.markdown("Mapa de calor que muestra cómo se relacionan numéricamente las variables clave.")
    columnas = ['Unit price', 'Quantity', 'Tax 5%', 'Total', 'cogs', 'gross income', 'Rating']
    corr = df[columnas].corr()
    fig, ax = plt.subplots(figsize=(10, 7))
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
    ax.set_title("Correlación Numérica")
    st.pyplot(fig)

# Análisis 8
elif analisis == "Ingreso Bruto por Sucursal y Línea":
    st.subheader("🏪 Ingreso Bruto por Sucursal y Línea de Producto")
    st.markdown("Explora qué líneas de producto generan más ingreso en cada sucursal.")
    resumen = df.groupby(['Branch', 'Product line'])['gross income'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=resumen, x='Branch', y='gross income', hue='Product line', ax=ax)
    ax.set_title("Ingreso Bruto por Sucursal y Línea de Producto")
    st.pyplot(fig)
