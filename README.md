# Aplikasi Form IDP 2026 - BPKOP NTB (Streamlit)

## Menjalankan
```
pip install -r requirements.txt
streamlit run app.py
```

## 1. Kirim jawaban ke Google Form (sekali setup)
Formulir yang sudah ada hanya memuat bagian profil dan rencana aksi. Agar **semua isian** (refleksi peran, gap kompetensi,
rencana pengembangan, optimalisasi peran) ikut masuk, buat form lengkap dengan skrip yang disediakan:
1. Buka https://script.google.com > **Proyek baru**.
2. Tempel seluruh isi `buat_google_form.gs`, simpan, pilih fungsi `buatFormIDP`, klik **Jalankan**, setujui izin.
3. Buka **Execution log**. Salin blok `GFORM_URL = ...` dan `[GFORM_ENTRIES] ...` ke `.streamlit/secrets.toml`
   (gantikan baris `GFORM_URL = ""` dan tabel `[GFORM_ENTRIES]` yang kosong).
4. Jalankan ulang aplikasi. Tab **Kirim** akan menyebut "Google Form" sebagai tujuan.
Jawaban muncul di tab **Responses** pada form tersebut, dan bisa dihubungkan ke Google Sheets.

## 2. Kirim ke email (opsional)
Isi `SMTP_USER` dan `SMTP_PASSWORD` (App Password Gmail) di `secrets.toml`. Penerima: `EMAIL_TO`.

## Deploy ke Streamlit Community Cloud
Unggah folder ke GitHub (tanpa `secrets.toml`), lalu tempel isi `secrets.toml` di **Settings > Secrets**.

## Catatan
- Pilihan dropdown di aplikasi dan form dibuat dari data yang sama, sehingga nilainya selalu cocok. Jika Anda mengubah
  pilihan di `app.py`, jalankan ulang skrip `.gs` yang baru atau samakan manual pilihan di form.
- Tanggal dikirim sebagai teks DD-MM-YYYY.
