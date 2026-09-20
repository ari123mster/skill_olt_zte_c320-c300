# Migrasi Windows / Linux

## Setup pertama
1. Instal KeePassXC dari https://keepassxc.org/ pada komputer tepercaya.
2. Di KeePassXC buat database baru bernama olt_credentials.kdbx di folder paket ini. Gunakan master passphrase kuat dan unik, diisi sendiri secara lokal. Jangan kirim ke chat. KDBX belum dibuat oleh paket karena memerlukan secret pengguna.
3. Key file opsional: simpan di lokasi terpisah dari paket/database dan cadangkan secara aman. Kehilangan komponen kunci dapat membuat database tidak dapat dipulihkan.
4. Buat grup OLT. Untuk setiap OLT_ID buat satu entry unik dalam grup, isi username/password. Excel Credential_Ref memakai OLT/<OLT_ID>. Password tidak masuk Excel.
5. Aktifkan auto-lock vault sesuai kebijakan. Hindari clipboard; jika digunakan, atur penghapusan clipboard otomatis dan waspadai clipboard history/sync.

## Migrasi
1. Tutup Excel dan KeePassXC. Buat backup database terenkripsi dan workbook sebelum transfer.
2. Salin seluruh folder paket, termasuk olt_connections.xlsx dan olt_credentials.kdbx jika sudah dibuat. Gunakan media/jalur transfer yang aman. Jangan salin master passphrase atau key file ke folder paket.
3. Instal KeePassXC pada tujuan. Python/openpyxl hanya diperlukan untuk helper workbook, bukan membaca skill.
4. Bandingkan checksum SHA-256 workbook/vault sumber dan tujuan. Nama drive/username tidak perlu sama; skill menggunakan path relatif root paket.
5. Buka vault pada tujuan dengan secret yang dimasukkan secara lokal. Jika memakai key file, sediakan melalui jalur terpisah.
6. Verifikasi jumlah entry, referensi OLT_ID dan username tanpa mengekspor password. Uji koneksi OLT secara terpisah hanya setelah persetujuan; verifikasi fingerprint SSH.
7. Jangan hapus sumber sebelum unlock dan pemeriksaan tujuan berhasil. Tidak ada penghapusan otomatis. Hindari editing vault paralel pada dua komputer.

## Perlindungan
Batasi permission file sesuai OS. Jangan commit Excel, vault, temporary atau backup ke Git. .gitignore bukan enkripsi dan tidak menghapus file yang sudah tracked. Backup harus terlindungi; key file tetap terpisah. Telnet tetap tidak terenkripsi meskipun password di KDBX aman.

## Status awal
Excel kosong telah dimigrasikan dari kolom Password ke Credential_Ref. Database KDBX belum dibuat; pengguna perlu menjalankan Setup pertama. Paket tidak memasang skill ke Hermes dan tidak mengaktifkan auto-login.
