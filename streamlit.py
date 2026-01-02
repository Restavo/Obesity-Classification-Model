import streamlit as st
import requests
import json
import pandas as pd


# Judul
st.title("Klasifikasi Tingkat Obesitas")
st.write("Membantu klasifikasi tingkat obesitas seseorang berdasarkan gaya hidup dan atribut fisik.")


# URL dari backend FastAPI 
API_URL = "http://127.0.0.1:8000/predict"

# Membuat form untuk input data pengguna
st.header("Masukkan Data Diri Anda")

with st.form(key='prediction_form'):
    # Menggunakan kolom agar layout lebih rapi
    col1, col2 = st.columns(2)

    with col1:
        Gender = st.selectbox("Jenis Kelamin (Gender)", ["Male", "Female"])
        Age = st.number_input("Usia (Age)", min_value=1, max_value=100, value=25)
        Height = st.number_input("Tinggi Badan (Height, dalam meter)", min_value=1.0, max_value=2.5, value=1.75, format="%.2f")
        Weight = st.number_input("Berat Badan (Weight, dalam kg)", min_value=20.0, max_value=200.0, value=70.0, format="%.1f")
        family_history_with_overweight = st.selectbox("Riwayat Keluarga Obesitas", ["yes", "no"])
        FAVC = st.selectbox("Sering Konsumsi Makanan Kalori Tinggi (FAVC)", ["yes", "no"])
        FCVC = st.slider("Frekuensi Konsumsi Sayuran (FCVC)", 1.0, 3.0, 2.0, 0.5)
        NCP = st.slider("Jumlah Makan Utama per Hari (NCP)", 1.0, 4.0, 3.0, 1.0)
        
    with col2:
        CAEC = st.selectbox("Konsumsi Makanan di Antara Waktu Makan (CAEC)", ["no", "Sometimes", "Frequently", "Always"])
        SMOKE = st.selectbox("Apakah Anda Merokok (SMOKE)?", ["yes", "no"])
        CH2O = st.slider("Asupan Air Harian (CH2O, dalam liter)", 1.0, 3.0, 2.0, 0.5)
        SCC = st.selectbox("Memantau Asupan Kalori (SCC)?", ["yes", "no"])
        FAF = st.slider("Frekuensi Aktivitas Fisik (FAF, hari per minggu)", 0.0, 3.0, 1.0, 0.5)
        TUE = st.slider("Waktu Menggunakan Teknologi (TUE, jam per hari)", 0.0, 2.0, 1.0, 0.5)
        CALC = st.selectbox("Frekuensi Konsumsi Alkohol (CALC)", ["no", "Sometimes", "Frequently"])
        MTRANS = st.selectbox("Moda Transportasi Utama (MTRANS)", ["Automobile", "Motorbike", "Bike", "Public_Transportation", "Walking"])

    # Tombol submit
    submit_button = st.form_submit_button(label='Prediksi')


# Jika tombol ditekan
if submit_button:
    # Kumpulkan data input ke dalam format dictionary
    input_data = {
        "Gender": Gender,
        "Age": Age,
        "Height": Height,
        "Weight": Weight,
        "family_history_with_overweight": family_history_with_overweight,
        "FAVC": FAVC,
        "FCVC": FCVC,
        "NCP": NCP,
        "CAEC": CAEC,
        "SMOKE": SMOKE,
        "CH2O": CH2O,
        "SCC": SCC,
        "FAF": FAF,
        "TUE": TUE,
        "CALC": CALC,
        "MTRANS": MTRANS,
    }

    # Kirim request ke API backend
    try:
        response = requests.post(API_URL, json=input_data)
        response.raise_for_status() 
        
        # Ambil hasil prediksi
        result = response.json()
        predicted_level = result['predicted_level']

        # Tampilkan hasil prediksi
        st.success(f"**Hasil Prediksi Tingkat Obesitas:** `{predicted_level}`")

    except requests.exceptions.RequestException as e:
        st.error(f"Error: {e}")
    except Exception as e:
        st.error(f"Eror: {e}")