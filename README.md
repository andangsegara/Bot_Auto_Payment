# Telegram Paid Link Bot (Manual Payment)

Bot Telegram untuk membuat link berbayar:
- Admin buat link dengan /buatlink <harga> <judul>|<konten>.
- User klik link → lihat harga + instruksi transfer manual.
- User dapatkan order_id.
- Admin konfirmasi manual dengan /markpaid <order_id>.
- Setelah konfirmasi, user bisa akses konten dengan /cek <order_id>.

## Setup
1. Clone repo.
2. pip install -r requirements.txt
3. Isi config.py dengan token & user_id admin.
4. Jalankan: python bot.py

## Notes
- Cocok untuk pembayaran manual (transfer bank, e-wallet).
- Jika ingin otomatis, bisa ganti modul pembayaran dengan integrasi QRIS/gateway.