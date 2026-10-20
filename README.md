# Aplikasi Form IDP 2026 (Streamlit)

## Menjalankan
```
pip install -r requirements.txt
cp .streamlit/secrets.toml.example .streamlit/secrets.toml   # lalu isi
streamlit run app.py
```

## Mengaktifkan kirim email
Email dikirim lewat SMTP dari akun pengirim ke `el.ulum82@gmail.com` (bisa diubah via `EMAIL_TO`).
Untuk Gmail:
1. Aktifkan verifikasi 2 langkah pada akun pengirim.
2. Buat **App Password** di https://myaccount.google.com/apppasswords.
3. Isi `SMTP_USER` dan `SMTP_PASSWORD` (App Password, bukan password biasa) di `secrets.toml`.

Jangan menaruh password di dalam `app.py` dan jangan commit `secrets.toml`.

## Deploy ke Streamlit Community Cloud
Unggah folder ke GitHub, buat app baru dari `app.py`, lalu isi isi `secrets.toml` pada menu
**Settings > Secrets**.

## Alur
Peserta mengisi 8 tab; tombol **Periksa & kirim ke email** memvalidasi isian wajib, lalu mengirim ringkasan
(.txt) dan data (.csv) sebagai lampiran. Jika email gagal, ringkasan tetap bisa diunduh.
