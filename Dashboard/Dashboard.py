import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import linregress

# Konfigurasi halaman Streamlit
st.set_page_config(
    page_title='🌫️ Analisis Pencemaran PM2.5 di Guanyuan',
    page_icon='🌫️',
    layout='wide'
)

# Fungsi untuk membaca data
@st.cache_data
def load_data():
    return pd.read_csv('Dashboard/all_data.csv', parse_dates=['date'])

# Fungsi visualisasi rata-rata PM2.5 per jam
def plot_hourly_pm25(data):
    hourly_pm25 = data.groupby(data['date'].dt.hour)['PM2.5'].mean()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    hourly_pm25.plot(kind='line', color='#5DADE2', ax=ax, linewidth=2)
    ax.set_title('Rata-rata PM2.5 Berdasarkan Jam dalam Sehari', fontsize=15, color='#34495E')
    ax.set_xlabel('Jam', fontsize=12)
    ax.set_ylabel('PM2.5 (mikrogram/m³)', fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    
    return fig

# Fungsi visualisasi hubungan faktor meteorologi dengan PM2.5
def plot_meteorological_factor(data, factor):
    correlation = data[['PM2.5', factor]].corr().iloc[0, 1]
    slope, intercept, _, _, _ = linregress(data[factor], data['PM2.5'])
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(x=factor, y='PM2.5', data=data, alpha=0.6, color='#FF7F50', ax=ax)
    ax.plot(data[factor], slope * data[factor] + intercept, color='red', label=f'Korelasi: {correlation:.2f}')
    ax.set_title(f'Hubungan {factor} dan PM2.5', fontsize=15, color='#34495E')
    ax.set_xlabel(f'{factor}', fontsize=12)
    ax.set_ylabel('PM2.5 (mikrogram/m³)', fontsize=12)
    ax.legend(fontsize=10)
    ax.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    
    return fig

# Fungsi untuk menampilkan catatan penting
def display_notes():
    st.markdown("""
    ### 📌 Catatan Penting
    - **Konsentrasi PM2.5** di Guanyuan cenderung **lebih rendah pada siang hari**, karena udara bergerak ke atas membantu menyebarkan polutan.
    - Konsentrasi **tertinggi terjadi pada malam hari**, karena udara dingin dekat permukaan tanah menjebak polutan.
    - **Kecepatan angin** adalah faktor meteorologi paling signifikan, dengan korelasi negatif **-0.28**, yang berarti semakin tinggi kecepatan angin, semakin rendah konsentrasi PM2.5.
    """)

# Main dashboard
st.title('🌫️ Analisis Pencemaran PM2.5 di Guanyuan')
st.markdown("Aplikasi ini membantu menganalisis pola harian dan pengaruh faktor meteorologi terhadap pencemaran udara.")

# Load data
data = load_data()

# Ringkasan Data
st.sidebar.header('📊 Ringkasan Data')
st.sidebar.write("**Rata-rata PM2.5**: {:.2f} µg/m³".format(data['PM2.5'].mean()))
st.sidebar.write("**PM2.5 Maksimum**: {:.2f} µg/m³".format(data['PM2.5'].max()))
st.sidebar.write("**PM2.5 Minimum**: {:.2f} µg/m³".format(data['PM2.5'].min()))
st.sidebar.write("Dataset terdiri dari {} baris dan {} kolom.".format(data.shape[0], data.shape[1]))
st.sidebar.markdown("---")

# Pola Harian PM2.5
st.header('🌅 Pola Harian PM2.5')
st.markdown("**Analisis pola rata-rata PM2.5 berdasarkan jam dalam sehari.**")
fig_hourly = plot_hourly_pm25(data)
st.pyplot(fig_hourly)

# Faktor Meteorologi
st.header('🌬️ Faktor Meteorologi')
factors = ['TEMP', 'RAIN', 'PRES', 'DEWP', 'WSPM']
selected_factor = st.selectbox("Pilih faktor meteorologi untuk dianalisis:", factors)

fig_factor = plot_meteorological_factor(data, selected_factor)
st.pyplot(fig_factor)

# Tabel korelasi horizontal
st.subheader('📈 Korelasi Faktor Meteorologi dengan PM2.5')
correlation = data[['PM2.5'] + factors].corr()['PM2.5'][factors]

# Ubah tabel menjadi horizontal dengan menggunakan transpose (.T)
correlation_df = pd.DataFrame(correlation).T
st.dataframe(correlation_df)


# Catatan penting
display_notes()

# Footer
st.markdown("""
---
<div style='text-align: center; color: grey;'>Dibuat oleh Rashad Muhammad Fajar | Data diolah menggunakan Python & Streamlit</div>
""", unsafe_allow_html=True)
