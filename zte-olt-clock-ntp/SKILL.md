---
name: zte-olt-clock-ntp
description: Atur waktu, zona waktu dan NTP pada OLT ZTE.
version: 0.1.0
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [zte, olt, clock, ntp, timezone]
    related_skills: [zte-olt-bootstrap-management]
---
# Waktu dan NTP

## Persetujuan pengguna untuk eksekusi berisiko

Wajib minta dan tunggu persetujuan eksplisit pengguna sebelum setiap eksekusi berisiko. Permintaan diagnosis, aktivasi umum, pembuatan skill, atau persetujuan sebelumnya bukan izin untuk tindakan baru.

Sebelum meminta izin, tampilkan target pelanggan/SN/interface/slot, perintah atau kelompok perubahan yang tepat (rahasia disamarkan), dampak layanan/keamanan, potensi kehilangan konfigurasi, dan rencana pemulihan. Eksekusi hanya tindakan dalam lingkup yang disetujui. Pengguna boleh menyetujui satu kelompok perintah yang sudah dijelaskan; perubahan target, perintah, dampak atau langkah pemulihan memerlukan persetujuan baru. Diam atau jawaban ambigu bukan persetujuan.

Termasuk berisiko: registrasi/penghapusan/ganti SN ONU; perubahan VLAN, WAN, port, profile, bandwidth, ACS, Wi-Fi, routing dan akses management; shutdown/unlock/aktivasi PON; DHCP renew; reboot/factory reset/reset-card/swap; perubahan akun/password/SSH/Telnet/SNMP/waktu; penonaktifan proteksi; pembukaan akses remote; serta `write` atau penyimpanan permanen. Rollback yang mengubah perangkat juga harus tercakup izin atau dimintakan izin baru.

Pembacaan status biasa pada target yang sudah diotorisasi dapat dilakukan tanpa izin mutasi tambahan. Jika tingkat risiko tidak jelas, berhenti dan tanyakan. Jangan melanjutkan mutasi otomatis setelah error, timeout atau putus koneksi: periksa kondisi secara baca-saja, lalu minta persetujuan baru bila tindakan lanjutan diperlukan. Dalam proses tanpa pengguna hadir, jangan lakukan tindakan berisiko tanpa persetujuan spesifik yang sudah tercatat.

## Kapan Digunakan
Log tidak sinkron atau operator meminta konfigurasi waktu. Bukan perubahan otomatis saat aktivasi pelanggan.
## Prosedur
1. Rekam `show clock` dan `show ntp status`; konfirmasi timezone dan server NTP tepercaya yang dapat dijangkau.
2. Setelah izin, contoh timezone sumber adalah GMT+7; gunakan offset lokasi aktual:
```text
configure terminal
clock timezone gmt <OFFSET>
ntp server <NTP_IP> priority <PRIORITY>
ntp enable
exit
```
3. Alternatif set manual dari privileged mode, bukan bersamaan dengan NTP aktif tanpa alasan:
```text
clock set <HH:MM:SS> <MONTH> <DAY> <YEAR>
show clock
```
4. Hanya atas permintaan penghapusan/penonaktifan, dalam global configuration:
```text
no ntp server <NTP_IP>
no ntp enable
```
Pilih operasi yang diminta, bukan menjalankan seluruh blok sebagai satu alur.
## Pitfalls
Perubahan jam dapat mengacaukan urutan histori/log. IP server dan tanggal contoh bukan default produksi. Verifikasi grammar offset/month dan prioritas firmware; jangan menebak rentang. Sumber tidak memberi sintaks autentikasi NTP.
## Verifikasi
Ulangi `show clock` dan `show ntp status`; catat zona waktu dan status sinkron aktual. Server terkonfigurasi belum berarti synchronized. Jangan mengaku sinkron ketika masih LOCAL/unsynchronized.

## Prasyarat dan pengaman
Template CLI perangkat, bukan shell OS. Validasi target/firmware dan input; tolak newline atau pemisah command. Rekam kondisi awal, rencana pemulihan, lalu minta persetujuan perubahan spesifik. Operator memasukkan rahasia melalui jalur aman; jangan meminta password/community di chat. Redaksi rahasia dari output. Jangan menyimpan permanen tanpa verifikasi dan izin. Sintaks C320 tidak dijamin untuk semua C300/model firmware.
