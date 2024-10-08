import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

hour_df = pd.read_csv("day.csv")
day_df = pd.read_csv("hour.csv")

def detect_outliers(df, column):
    q25, q75 = np.percentile(df[column], 25), np.percentile(df[column], 75)
    iqr = q75 - q25
    cut_off = iqr*1.5
    minimum, maximum = q25 - cut_off, q75 + cut_off

    return (df[column] < minimum) | (df[column] > maximum)

hour_df_masked = hour_df.mask(detect_outliers(hour_df, 'registered'))
hour_df_masked = hour_df_masked.mask(detect_outliers(hour_df_masked, 'cnt'))

hour_df_cleaned = hour_df_masked.dropna()
print(hour_df_cleaned.head())

day_df_masked = day_df.mask(detect_outliers(day_df, 'registered'))
day_df_masked = day_df_masked.mask(detect_outliers(day_df_masked, 'cnt'))

day_df_cleaned = day_df_masked.dropna()
print(day_df_cleaned.head())

hour_df.describe(include="all")
day_df.describe(include="all")

busiest_hour = hour_df_cleaned.loc[hour_df_cleaned['cnt'].idxmax()]
least_busy_hour = hour_df_cleaned.loc[hour_df_cleaned['cnt'].idxmin()]

day_df_cleaned = day_df_masked.dropna()

# Mencari jam paling sibuk dan paling tidak sibuk
busiest_hour = hour_df_cleaned.loc[hour_df_cleaned['cnt'].idxmax()]
least_busy_hour = hour_df_cleaned.loc[hour_df_cleaned['cnt'].idxmin()]

# Membuat plot
fig, ax = plt.subplots(figsize=(6,2))
sns.lineplot(data=hour_df_cleaned, x='hr', y='cnt', marker="o")
ax.set_title('PENGGUNAAN SEPEDA BERDASARKAN JAM')
ax.set_xlabel('Jam dalam sehari')
ax.set_ylabel('Jumlah pengguna Sepeda')

# Membuat bar chart
fig2, ax2 = plt.subplots(figsize=(6,2))
sns.barplot(data=hour_df_cleaned, x='hr', y='cnt')
ax2.set_title('PENGGUNAAN SEPEDA BERDASARKAN JAM (BAR CHART)')
ax2.set_xlabel('Jam dalam sehari')
ax2.set_ylabel('Jumlah pengguna Sepeda')

# Membuat aplikasi Streamlit
st.title("Analisis Penggunaan Sepeda")
st.header("Hasil Analisis")

# Menampilkan hasil analisis
st.write("Jam paling sibuk: ", busiest_hour['hr'])
st.write("Jumlah pengguna sepeda pada jam paling sibuk: ", busiest_hour['cnt'])
st.write("Jam paling tidak sibuk: ", least_busy_hour['hr'])
st.write("Jumlah pengguna sepeda pada jam paling tidak sibuk: ", least_busy_hour['cnt'])

# Menampilkan plot
st.pyplot(fig)

# Menampilkan bar chart
st.pyplot(fig2)

# Menambahkan opsi untuk menampilkan data mentah
if st.checkbox("Show raw data"):
    st.write(hour_df_cleaned)
