import streamlit as st #NOSSSA INTERFACE
import pandas as pd #GRAFICOS E DADOS
import numpy as np #MANIPULACAO NUMERICA

st.title('CORRIDAS DE UBER EM NOVA YORK')

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')
@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data(10000)
# Notify the reader that the data was successfully loaded.
data_load_state.text("Done! (using st.cache_data)")

if st.checkbox('Mostrar dados brutos'):
    st.subheader('Dados brutos')
    st.write(data)

st.subheader('Número de corridas por hora')

hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values,x_label="hora", y_label="nª pedidos",width=5000,color="#61D921")

hour_to_filter = st.slider('hora', 0, 23, 17)  # min: 0h, max: 23h, default: 17h
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader(f'Mapa de todos os pedidos às {hour_to_filter}:00')
st.map(filtered_data)

