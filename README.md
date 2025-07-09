
# Aplikasi Akuntansi UMKM Web

Aplikasi akuntansi sederhana untuk pelaku UMKM, berbasis Flask dan mendukung login multi-user.

## Fitur:
- Tambah transaksi pemasukan/pengeluaran
- Laporan keuangan otomatis (saldo, income, expense)
- Login dan logout untuk tiap pengguna
- Siap untuk di-deploy secara online

## 📦 Cara Install di Lokal

```bash
pip install -r requirements.txt
python app.py
```

Lalu buka browser ke `http://localhost:5000`

## 🚀 Cara Deploy ke Railway/Render/Heroku

1. Buat akun di [render.com](https://render.com), [railway.app](https://railway.app), atau [heroku.com](https://heroku.com)
2. Upload file:
   - `app.py`
   - `requirements.txt`
   - `Procfile`
3. Jalankan layanan web (port default 5000)
4. Akses aplikasi online dari domain yang diberikan

## Lisensi
Gratis digunakan, diedit, dan dikembangkan kembali.
