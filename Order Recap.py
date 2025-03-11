import pandas as pd
import streamlit as st
import altair as alt

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
        no_pesanan = st.sidebar.text_input("No. Pesanan")
        no_resi = st.sidebar.text_input("No. Resi")
        opsi_pengiriman = st.sidebar.text_input("Opsi Pengiriman")
        metode_pembayaran = st.sidebar.text_input("Metode Pembayaran")
        provinsi = st.sidebar.text_input("Provinsi")
        
        # Filter data berdasarkan input pengguna
        if no_pesanan:
            df = df[df["No. Pesanan"].astype(str).str.contains(no_pesanan, na=False, case=False)]
        if no_resi:
            df = df[df["No. Resi"].astype(str).str.contains(no_resi, na=False, case=False)]
        if opsi_pengiriman:
            df = df[df["Opsi Pengiriman"].astype(str).str.contains(opsi_pengiriman, na=False, case=False)]
        if metode_pembayaran:
            df = df[df["Metode Pembayaran"].astype(str).str.contains(metode_pembayaran, na=False, case=False)]
        if provinsi:
            df = df[df["Provinsi"].astype(str).str.contains(provinsi, na=False, case=False)]
        
        st.write("### Data setelah filter:")
        st.dataframe(df)
    else:
        st.warning("Sheet 'Data Orders' tidak ditemukan dalam file Excel.")
