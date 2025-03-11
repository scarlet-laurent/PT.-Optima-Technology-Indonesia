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
    
    if "Data Orders" in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name="Data Orders")

        # Konversi kolom tanggal ke datetime jika ada
        if 'Waktu Pesanan Selesai' in df.columns:
            df['Waktu Pesanan Selesai'] = pd.to_datetime(df['Waktu Pesanan Selesai'], errors='coerce').dt.date
            df = df.dropna(subset=['Waktu Pesanan Selesai'])  # Hapus NaT jika ada
        
        st.write("### Data yang diunggah (Sheet: Data Orders):")
        st.dataframe(df)

        # **Filter Tanggal**
        st.write("### Waktu Pesanan Selesai")
        min_value = df['Waktu Pesanan Selesai'].min()
        max_value = df['Waktu Pesanan Selesai'].max()

        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Dari Tanggal", value=min_value, min_value=min_value, max_value=max_value)
        with col2:
            end_date = st.date_input("Sampai Tanggal", value=max_value, min_value=min_value, max_value=max_value)
        
        # Terapkan filter tanggal
        df = df.loc[(df['Waktu Pesanan Selesai'] >= start_date) & (df['Waktu Pesanan Selesai'] <= end_date)]

        # **Filter Sidebar**
        st.sidebar.header('Filters')
        filter_columns = {
            "No. Pesanan": "No. Pesanan",
            "No. Resi": "No. Resi",
            "Opsi Pengiriman": "Opsi Pengiriman",
            "Metode Pembayaran": "Metode Pembayaran",
            "Provinsi": "Provinsi",
        }

        for label, column in filter_columns.items():
            if column in df.columns:
                selected = st.sidebar.multiselect(label, df[column].dropna().unique())
                if selected:
                    df = df[df[column].isin(selected)]

        st.write("### Data setelah filter:")
        if df.empty:
            st.warning("Tidak ada data yang sesuai dengan filter yang dipilih.")
        else:
            st.dataframe(df)

        # **Order Recap**
        st.header('Order Recap', divider='gray')

        if 'Waktu Pesanan Selesai' in df.columns and 'No. Pesanan' in df.columns:
            completed_orders = df['No. Pesanan'].nunique()
            fake_orders = df[df.get('Fake List Order', '') == 'Fake Order']['No. Pesanan'].nunique() if 'Fake List Order' in df.columns else 0

            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                    <p style='font-size: 20px; text-align: center;'>
                        <strong>Total Pesanan Selesai: <span style='color: green;'>{completed_orders:,}</span></strong>
                    </p>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown(f"""
                    <p style='font-size: 20px; text-align: center;'>
                        <strong>Fake Order: <span style='color: red;'>{fake_orders:,}</span></strong>
                    </p>
                """, unsafe_allow_html=True)
        else:
            st.warning("Kolom yang diperlukan tidak ditemukan dalam file Excel.")
