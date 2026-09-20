---
name: zte-olt-connection-inventory
description: Kelola inventaris OLT dan vault KeePass lintas OS.
version: 0.2.0
platforms: [linux, macos, windows]
---

# Inventaris OLT dan KeePassXC

## Persetujuan pengguna untuk eksekusi berisiko

Wajib minta dan tunggu persetujuan eksplisit pengguna sebelum setiap eksekusi berisiko. Permintaan diagnosis, aktivasi umum, pembuatan skill, atau persetujuan sebelumnya bukan izin untuk tindakan baru.

Sebelum meminta izin, tampilkan target pelanggan/SN/interface/slot, perintah atau kelompok perubahan yang tepat (rahasia disamarkan), dampak layanan/keamanan, potensi kehilangan konfigurasi, dan rencana pemulihan. Eksekusi hanya tindakan dalam lingkup yang disetujui. Pengguna boleh menyetujui satu kelompok perintah yang sudah dijelaskan; perubahan target, perintah, dampak atau langkah pemulihan memerlukan persetujuan baru. Diam atau jawaban ambigu bukan persetujuan.

Termasuk berisiko: registrasi/penghapusan/ganti SN ONU; perubahan VLAN, WAN, port, profile, bandwidth, ACS, Wi-Fi, routing dan akses management; shutdown/unlock/aktivasi PON; DHCP renew; reboot/factory reset/reset-card/swap; perubahan akun/password/SSH/Telnet/SNMP/waktu; penonaktifan proteksi; pembukaan akses remote; serta `write` atau penyimpanan permanen. Rollback yang mengubah perangkat juga harus tercakup izin atau dimintakan izin baru.

Pembacaan status biasa pada target yang sudah diotorisasi dapat dilakukan tanpa izin mutasi tambahan. Jika tingkat risiko tidak jelas, berhenti dan tanyakan. Jangan melanjutkan mutasi otomatis setelah error, timeout atau putus koneksi: periksa kondisi secara baca-saja, lalu minta persetujuan baru bila tindakan lanjutan diperlukan. Dalam proses tanpa pengguna hadir, jangan lakukan tindakan berisiko tanpa persetujuan spesifik yang sudah tercatat.

## Kapan Digunakan
Menambah/memperbarui profil koneksi OLT SSH/Telnet atau memigrasikan inventaris Windows/Linux. Tidak membuat akun OLT atau login otomatis.

## Penyimpanan
Root paket adalah parent direktori skill, bukan working directory atau drive Windows tetap.
- `../olt_connections.xlsx`, sheet OLT: OLT_ID, Nama_OLT, Host, Protocol, Port, Username, Credential_Ref, Catatan.
- `../olt_credentials.kdbx`: database KeePassXC terenkripsi, dibuat pengguna secara lokal.
- Credential_Ref berupa path entry `OLT/<OLT_ID>`; judul entry harus unik dalam grup OLT. Username di vault dan inventaris harus konsisten; password hanya di vault.
- Master passphrase dan key file tidak boleh disimpan dalam folder paket, script, Excel, chat, log atau memory agent. Database dan Excel boleh satu folder; key file harus terpisah.

## Prasyarat
KeePassXC pada Windows/Linux. Untuk workbook, Python dan openpyxl (opsional `uv run --with openpyxl python ...`). Jangan menganggap executable berada di PATH; identifikasi lokasi instalasi tanpa menjalankannya dengan password sebagai argument. Gunakan fungsi UI KeePassXC yang tersedia untuk pembuatan database. Tidak ada integrasi auto-login dalam paket ini.

## Prosedur
1. Tanyakan ID/nama OLT, IP/hostname, SSH/Telnet, port dan username. SSH 22/Telnet 23 hanya saran, konfirmasi port aktual. Jangan meminta password di chat.
2. Jika vault belum ada, pengguna membuat database KeePassXC di root paket dengan nama `olt_credentials.kdbx`, memilih master passphrase kuat secara lokal. Opsional key file disimpan terpisah dan dicadangkan. Agent tidak mengetik atau menyimpan rahasia. Jangan membuat vault dengan password contoh, kosong atau key hardcoded.
3. Pengguna membuat grup OLT dan entry berjudul OLT_ID; mengisi username/password di KeePassXC. Catat Credential_Ref `OLT/<OLT_ID>` di Excel, bukan password atau master passphrase. Jangan mengekspor vault ke CSV/XML plaintext.
4. Validasi ID unik; host IP/hostname tanpa scheme/path/port inline; protocol SSH/TELNET; port integer 1–65535; field wajib tidak kosong. Tolak control character/newline atau pemisah command. Tulis input sebagai string literal, bukan formula. Path referensi harus cocok entry unik, bukan ditebak dari nama pelanggan.
5. Tampilkan metadata dan perubahan tanpa rahasia. Minta persetujuan penambahan/perubahan profil. Jangan menimpa entry existing atau merotasi password OLT akibat perubahan inventory. Sinkronkan username metadata jika diubah.
6. Tutup Excel sebelum save. Baca ulang file terbaru, pertahankan sheet/baris lain, simpan temporary di folder sama, validasi lalu replace atomik. Batalkan jika file berubah atau terkunci. Backup workbook/vault sebelum perubahan sesuai izin; jangan membuat backup plaintext password.
7. Operator memverifikasi Credential_Ref ada dan username cocok saat vault dibuka. Laporan cukup referensi tersedia/tidak ada dan metadata; tidak ada dump password.

## Pemakaian dan migrasi
Gunakan panduan `../MIGRASI.md`. Pilih OLT_ID eksplisit sebelum koneksi; vault bukan izin menjalankan command OLT. Untuk tahap ini operator unlock vault dan menggunakan kredensial melalui aplikasi koneksi secara lokal. Otomasi masa depan harus memakai integrasi yang tidak mengirim rahasia ke model, command-line argument atau stdout; jangan improvisasi `keepassxc-cli show -s` yang mencetak password.

Salin workbook, vault, dan skill menggunakan jalur relatif. Bandingkan SHA-256 sebelum/sesudah transfer tanpa mencetak isi. Uji unlock pada tujuan dan referensi entry sebelum menghapus sumber. Jangan simpan key file bersama backup database. Jangan edit dua salinan vault secara bersamaan tanpa prosedur merge/backup yang disepakati.

## Pitfalls
KDBX terenkripsi tidak melindungi rahasia saat vault terbuka pada mesin tersusupi. Excel tetap memuat metadata sensitif; batasi ACL Windows/permission Linux. Jangan chmod/chown atau mengubah ACL otomatis tanpa persetujuan. Sheet protection bukan enkripsi. Telnet mengirim password tanpa enkripsi; hanya jaringan terisolasi dengan izin risiko. Jika ada password plaintext lama, jangan menghapus sebelum import vault dan unlock berhasil diverifikasi; ekspor/backup lama juga harus ditangani atas izin pengguna.

## Verifikasi
Workbook tidak memiliki kolom Password atau formula input. Template awal nol profil. File vault belum dianggap tersedia sampai pengguna membuatnya dan berhasil unlock. Lakukan round-trip migrasi satu referensi tanpa menampilkan secret. Jangan mengaku koneksi OLT berhasil dari validasi file saja.

