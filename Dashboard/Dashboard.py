import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import linregress

# Konfigurasi halaman Streamlit
st.set_page_config(page_title='Analisis Pencemaran PM2.5 di Guanyuan', layout='wide')

# Fungsi untuk membaca data
@st.cache_data
def load_data():
    return pd.read_csv('Dashboard/all_data.csv', parse_dates=['date'])

# Fungsi visualisasi rata-rata PM2.5 per jam
def plot_hourly_pm25(data):
    hourly_pm25 = data.groupby(data['date'].dt.hour)['PM2.5'].mean()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    hourly_pm25.plot(kind='line', color='skyblue', ax=ax)
    ax.set_title('Rata-rata PM2.5 Berdasarkan Jam dalam Sehari', fontsize=15)
    ax.set_xlabel('Jam', fontsize=12)
    ax.set_ylabel('PM2.5 (mikrogram/m³)', fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.7)
    
    return fig

# Fungsi visualisasi hubungan faktor meteorologi dengan PM2.5
def plot_meteorological_factors(data, factors):
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    axes = axes.flatten()
    
    correlation = data[['PM2.5'] + factors].corr()
    
    for i, factor in enumerate(factors):
        # Korelasi antara faktor saat ini dan PM2.5
        corr_value = correlation.loc['PM2.5', factor]
        
        # Scatterplot
        sns.scatterplot(x=factor, y='PM2.5', data=data, alpha=0.5, ax=axes[i])
        
        # Garis tren
        slope, intercept, r_value, p_value, std_err = linregress(data[factor], data['PM2.5'])
        axes[i].plot([data[factor].min(), data[factor].max()], 
                    [slope * data[factor].min() + intercept, 
                     slope * data[factor].max() + intercept], 
                    color='red', label=f'y = {slope:.2f}x + {intercept:.2f}\nr = {r_value:.2f}')
        
        axes[i].set_title(f'Hubungan {factor} dan PM2.5', fontsize=12)
        axes[i].set_xlabel(f'{factor}', fontsize=10)
        axes[i].set_ylabel('PM2.5 (mikrogram/m³)', fontsize=10)
        axes[i].legend()
    
    # Matikan subplot kosong jika ada
    for i in range(len(factors), len(axes)):
        axes[i].axis('off')
    
    plt.tight_layout()
    return fig

# Main dashboard
def main():
    st.title('🌫️ Analisis Pencemaran PM2.5')
    
    # Load data
    data = load_data()
    
    # Sidebar untuk navigasi
    st.sidebar.title('Navigasi')
    menu = st.sidebar.radio('Pilih Analisis', 
                             ['Ringkasan Data', 
                              'Pola Harian PM2.5', 
                              'Faktor Meteorologi'])
    
    # Ringkasan Data
    if menu == 'Ringkasan Data':
        st.header('Ringkasan Data PM2.5')
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric('Rata-rata PM2.5', f"{data['PM2.5'].mean():.2f} µg/m³")
        with col2:
            st.metric('Maksimum PM2.5', f"{data['PM2.5'].max():.2f} µg/m³")
        with col3:
            st.metric('Minimum PM2.5', f"{data['PM2.5'].min():.2f} µg/m³")
        
        st.dataframe(data.head())
    
    # Pola Harian PM2.5
    elif menu == 'Pola Harian PM2.5':
        st.header('Waktu dengan Risiko Tinggi Pencemaran Udara')
        
        fig_hourly = plot_hourly_pm25(data)
        st.pyplot(fig_hourly)
        
        # Penjelasan tambahan
        st.markdown("""
        ### Interpretasi
        - Grafik menunjukkan rata-rata konsentrasi PM2.5 per jam
        - Identifikasi jam-jam dengan konsentrasi tertinggi sebagai waktu berisiko tinggi
        """)
    
    # Faktor Meteorologi
    elif menu == 'Faktor Meteorologi':
        st.header('Pengaruh Faktor Meteorologi terhadap PM2.5')
        
        factors = ['TEMP', 'RAIN', 'PRES', 'DEWP', 'WSPM']
        fig_factors = plot_meteorological_factors(data, factors)
        st.pyplot(fig_factors)
        
        # Tabel korelasi
        st.subheader('Korelasi Faktor Meteorologi dengan PM2.5')
        correlation = data[['PM2.5'] + factors].corr()['PM2.5'][factors]
        st.dataframe(correlation)
        
        st.markdown("""
        ### Interpretasi
        - Grafik scatter plot menunjukkan hubungan antara faktor meteorologi dan PM2.5
        - Garis merah menunjukkan trend linear
        - Semakin dekat nilai korelasi (r) ke 1 atau -1, semakin kuat hubungannya
        """)

if __name__ == '__main__':
    main()