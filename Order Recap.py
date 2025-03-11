import pandas as pd
import streamlit as st
import altair as alt
from datetime import datetime

# Set judul dan ikon pada browser
st.set_page_config(
    page_title='Data Penjualan PT Optima Technology Indonesia',
    page_icon='📈',
)

# Menampilkan logo di sidebar
st.sidebar.image('logo.png', use_container_width=True)

# Upload file Excel
st.title("Dashboard Analisis Penjualan")
uploaded_file = st.file_uploader("Unggah file Excel", type=["xlsx", "xls"])

if uploaded_file is not None:
    # Membaca data Excel
    xls = pd.ExcelFile(uploaded_file)
    
    # Pastikan sheet 'Data Orders' ada
    if "Data Orders" in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name="Data Orders")
        
        # Menampilkan data
        st.write("### Data yang diunggah (Sheet: Data Orders):")
        st.dataframe(df)
        
        # Add filters to the sidebar
        st.sidebar.header('Filters')
        no_pesanan = st.sidebar.multiselect("No. Pesanan", options=df["No. Pesanan"].dropna().unique())
        no_resi = st.sidebar.multiselect("No. Resi", options=df["No. Resi"].dropna().unique())
        opsi_pengiriman = st.sidebar.multiselect("Opsi Pengiriman", options=df["Opsi Pengiriman"].dropna().unique())
        metode_pembayaran = st.sidebar.multiselect("Metode Pembayaran", options=df["Metode Pembayaran"].dropna().unique())
        provinsi = st.sidebar.multiselect("Provinsi", options=df["Provinsi"].dropna().unique())
        
        # Filter data berdasarkan input pengguna
        if no_pesanan:
            df = df[df["No. Pesanan"].isin(no_pesanan)]
        if no_resi:
            df = df[df["No. Resi"].isin(no_resi)]
        if opsi_pengiriman:
            df = df[df["Opsi Pengiriman"].isin(opsi_pengiriman)]
        if metode_pembayaran:
            df = df[df["Metode Pembayaran"].isin(metode_pembayaran)]
        if provinsi:
            df = df[df["Provinsi"].isin(provinsi)]
        
        st.write("### Data setelah filter:")
        st.dataframe(df)
    else:
        st.warning("Sheet 'Data Orders' tidak ditemukan dalam file Excel.")
