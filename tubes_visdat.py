import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu

# Load data CSV
@st.cache_data
def load_data():
    return pd.read_csv('all_seasons.csv')

# Load dataset
df = load_data()

# Judul aplikasi
st.title("Interactive Basketball Player Stats Visualization")

if 'Unnamed: 0' in df.columns:
    df = df.drop(columns=['Unnamed: 0'])

# Navigation Bar
selected = option_menu(
    menu_title=None, 
    options=["Data Pemain", "Visualisasi Statistik", "Analisis Tinggi & Berat"], 
    icons=["table", "bar-chart", "activity"],  
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)

# Sidebar - Filter data
st.sidebar.header("Filter Data")
teams = st.sidebar.multiselect("Pilih Tim", df['team_abbreviation'].unique(), default=df['team_abbreviation'].unique())
seasons = st.sidebar.multiselect("Pilih Musim", df['season'].unique(), default=df['season'].unique())
age_range = st.sidebar.slider("Pilih Rentang Usia Pemain", int(df['age'].min()), int(df['age'].max()), (20, 35))

# Filter data berdasarkan pilihan pengguna
filtered_df = df[
    (df['team_abbreviation'].isin(teams)) & 
    (df['season'].isin(seasons)) & 
    (df['age'] >= age_range[0]) & 
    (df['age'] <= age_range[1])
]

# Konten berdasarkan halaman yang dipilih
if selected == "Data Pemain":
    st.title("Data Pemain Basket yang Dipilih")
    st.dataframe(filtered_df)

elif selected == "Visualisasi Statistik":
    st.title("Visualisasi Statistik Pemain")

    # Visualisasi: Scatter plot poin vs assist
    st.write("### Scatter Plot: Poin vs Assist")
    fig_scatter = px.scatter(filtered_df, x='pts', y='ast', color='team_abbreviation',
                             hover_data=['player_name', 'age', 'reb'],
                             title="Poin vs Assist per Pemain")
    st.plotly_chart(fig_scatter)

    # Visualisasi: Bar chart rata-rata poin per tim
    st.write("### Rata-rata Poin per Tim")
    avg_pts = filtered_df.groupby('team_abbreviation')['pts'].mean().reset_index()
    fig_bar = px.bar(avg_pts, x='team_abbreviation', y='pts', title="Rata-rata Poin per Tim")
    st.plotly_chart(fig_bar)

    # Visualisasi: Distribusi umur pemain
    st.write("### Distribusi Usia Pemain")
    fig_hist = px.histogram(filtered_df, x='age', nbins=15, title="Distribusi Usia Pemain")
    st.plotly_chart(fig_hist)

elif selected == "Analisis Tinggi & Berat":
    st.title("Analisis Tinggi dan Berat Badan Pemain")

    # Scatter plot: Tinggi vs Berat Badan
    st.write("### Scatter Plot: Tinggi vs Berat Badan Pemain")
    fig_height_weight = px.scatter(filtered_df, x='player_height', y='player_weight', 
                                   color='team_abbreviation', hover_data=['player_name', 'age'],
                                   title="Tinggi vs Berat Badan Pemain")
    st.plotly_chart(fig_height_weight)

    # Histogram: Distribusi Tinggi Badan
    st.write("### Distribusi Tinggi Badan")
    fig_height_hist = px.histogram(filtered_df, x='player_height', nbins=20, title="Distribusi Tinggi Badan Pemain")
    st.plotly_chart(fig_height_hist)

    # Histogram: Distribusi Berat Badan
    st.write("### Distribusi Berat Badan")
    fig_weight_hist = px.histogram(filtered_df, x='player_weight', nbins=20, title="Distribusi Berat Badan Pemain")
    st.plotly_chart(fig_weight_hist)

    # Rata-rata Tinggi dan Berat Badan per Tim
    st.write("### Rata-rata Tinggi dan Berat Badan per Tim")
    avg_height_weight = filtered_df.groupby('team_abbreviation')[['player_height', 'player_weight']].mean().reset_index()
    fig_avg_height_weight = px.bar(avg_height_weight, x='team_abbreviation', 
                                   y=['player_height', 'player_weight'], 
                                   title="Rata-rata Tinggi dan Berat Badan per Tim", 
                                   barmode='group')
    st.plotly_chart(fig_avg_height_weight)
