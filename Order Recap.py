import pandas as pd
import streamlit as st
import altair as alt

# Upload file Excel
st.title("Dashboard Analisis Penjualan")
uploaded_file = st.file_uploader("Unggah file Excel", type=["xlsx", "xls"])

if uploaded_file is not None:
    # Membaca data Excel
    xls = pd.ExcelFile(uploaded_file)
    sheet_names = xls.sheet_names
    
    # Pilih sheet untuk ditampilkan
    sheet_selected = st.selectbox("Pilih Sheet", sheet_names)
    df = pd.read_excel(xls, sheet_name=sheet_selected)
    
    # Menampilkan data
    st.write("### Data yang diunggah:")
    st.dataframe(df)
