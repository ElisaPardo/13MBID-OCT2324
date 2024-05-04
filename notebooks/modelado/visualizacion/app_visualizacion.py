import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
st.set_page_config(layout="wide")
# Se realiza la lectura de los datos
df = pd.read_csv("../../../data/final/datos_finales.csv", sep=";")

# Título del dashboard
st.write("# 13MBID - Visualización de datos")
st.write("## Panel de visualización generado sobre los datos de créditos y tarjetas emitidas a clientes de la entidad")
st.write("#### Persona: Elisa Pardo Cuenca")
st.write("----")

# Gráficos
st.write("### Caracterización de los créditos otorgados")

col1, col2= st.columns ([1,1], gap="medium")
# Se tienen que agregar las definiciones de gráficos desde la libreta
creditos_x_objetivo = px.histogram(df, x='objetivo_credito', 
                                   title='Conteo de créditos por objetivo')
creditos_x_objetivo.update_layout(xaxis_title='Objetivo del crédito', yaxis_title='Cantidad')

# Se realiza la "impresión" del gráfico en el dashboard
with col1:
    st.plotly_chart(creditos_x_objetivo,use_container_width=True)


# Histograma de los importes de créditos otorgados
histograma_importes = px.histogram(df, x='importe_solicitado', nbins=10, title='Importes solicitados en créditos')
histograma_importes.update_layout(xaxis_title='Importe solicitado', yaxis_title='Cantidad')

with col2:
    st.plotly_chart(histograma_importes,use_container_width=True)

# Filtros

option = st.selectbox(
    'Qué tipo de crédito desea filtrar?',
     df['objetivo_credito'].unique())

df_filtrado = df[df['objetivo_credito'] == option]

st.write(f"Tipo de crédito seleccionado: {option}")



if st.checkbox('Mostrar créditos finalizados?', value=True):

    # Conteo de ocurrencias por estado
    estado_credito_counts = df_filtrado['estado_credito_N'].value_counts()
    

    # Gráfico de torta de estos valores
    colors = ["light blue", "mediumturquoise"]
    fig = go.Figure(data=[go.Pie(labels=estado_credito_counts.index, values=estado_credito_counts, marker=dict(colors=colors))])
    fig.update_layout(title_text='Distribución de créditos por estado registrado', legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1 , title="Estado crédito"))

    fig2 = px.histogram(df_filtrado, x='tasa_interes', color='estado_credito_N', color_discrete_map={'C':"mediumturquoise", 'P':'light blue'},
                        barmode='group',nbins=4, title='Distribución de créditos según la tasa de interés por estado registrado', text_auto = True,
                   category_orders={"tasa_interes": ["hasta_7p", "7p_a_15p", "15p_a_20p", "mayor_20p"]})
    fig2.update_layout(xaxis_title='Tasa de interés', yaxis_title='Cantidad', legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1 , title="Estado crédito"))

else:
    df_filtrado = df_filtrado[df_filtrado['estado_credito_N'] == 'P']
    # Conteo de ocurrencias por caso
    falta_pago_counts = df_filtrado['falta_pago'].value_counts()

    # Create a Pie chart
    colors = ["light blue", "mediumturquoise"]
    fig = go.Figure(data=[go.Pie(labels=falta_pago_counts.index, values=falta_pago_counts, marker=dict(colors=colors))])
    fig.update_layout(title_text='Distribución de créditos en función de registro de mora',legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1 , title="Falta pago"))

    fig2 = px.histogram(df_filtrado, x='tasa_interes', color='falta_pago',color_discrete_map={'Y':"mediumturquoise", 'N':'light blue'},
                         barmode='group',nbins=4, title='Distribución de créditos según la tasa de interés en función de registro de mora', text_auto = True,
                   category_orders={"tasa_interes": ["hasta_7p", "7p_a_15p", "15p_a_20p", "mayor_20p"]})
    fig2.update_layout(xaxis_title='Tasa de interés', yaxis_title='Cantidad',legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1 , title="Falta pago"))

st.write(f"Cantidad de créditos con estas condiciones: {df_filtrado.shape[0]}")

col3, col4= st.columns ([1,1], gap="medium")
with col3:
    st.plotly_chart(fig, use_container_width=True)
with col4:  
    st.plotly_chart(fig2,use_container_width=True)