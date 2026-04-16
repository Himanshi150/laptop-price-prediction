import streamlit as st
import pickle
import numpy as np
import pandas as pd

# Load model and dataframe
pipe = pickle.load(open('pipe.pkl', 'rb'))
df = pickle.load(open('df.pkl', 'rb'))

st.title("Laptop Price Predictor")

# Inputs
company = st.selectbox('Brand', df['Company'].unique())
type = st.selectbox('Type', df['TypeName'].unique())
ram = st.selectbox('RAM (GB)', [2,4,6,8,12,16,24,32,64])

weight = st.number_input('Weight (kg)', min_value=0.5)

touchscreen = st.selectbox('Touchscreen', ['No','Yes'])
ips = st.selectbox('IPS', ['No','Yes'])

ppi = st.number_input('PPI', min_value=50.0)

cpu = st.selectbox('CPU brand', df['cpu brand'].unique())
hdd = st.selectbox('HDD (GB)', [0,128,256,512,1024,2048])
ssd = st.selectbox('SSD (GB)', [0,8,128,256,512,1024])
gpu = st.selectbox('GPU brand', df['Gpu brand'].unique())
os = st.selectbox('Operating System', df['os'].unique())

# Convert Yes/No to 1/0
touchscreen = 1 if touchscreen == 'Yes' else 0
ips = 1 if ips == 'Yes' else 0

# Create query dataframe
query = pd.DataFrame({
    'Company': [company],
    'TypeName': [type],
    'Ram': [ram],
    'Weight': [weight],
    'Touchscreen': [touchscreen],
    'Ips': [ips],
    'ppi': [float(ppi)],
    'cpu brand': [cpu],
    'HDD': [hdd],
    'SSD': [ssd],
    'Gpu brand': [gpu],
    'os': [os]
})
if st.button('Predict Price'):

    prediction = pipe.predict(query)[0]

    st.write("Prediction value:", prediction)

    if np.isfinite(prediction):
        price = int(prediction)
        st.title("The predicted price of this configuration is ₹ " + str(price))
    else:
        st.error("Invalid prediction. Please check input values.")