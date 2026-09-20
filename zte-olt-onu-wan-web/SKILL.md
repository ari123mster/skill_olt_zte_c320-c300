---
name: zte-olt-onu-wan-web
description: Atur akses web WAN ONT ZTE secara terbatas.
version: 0.1.0
platforms: [linux, macos, windows]
---

# Akses Web WAN ONT

## Persetujuan pengguna untuk eksekusi berisiko

Wajib minta dan tunggu persetujuan eksplisit pengguna sebelum setiap eksekusi berisiko. Permintaan diagnosis, aktivasi umum, pembuatan skill, atau persetujuan sebelumnya bukan izin untuk tindakan baru.

Sebelum meminta izin, tampilkan target pelanggan/SN/interface/slot, perintah atau kelompok perubahan yang tepat (rahasia disamarkan), dampak layanan/keamanan, potensi kehilangan konfigurasi, dan rencana pemulihan. Eksekusi hanya tindakan dalam lingkup yang disetujui. Pengguna boleh menyetujui satu kelompok perintah yang sudah dijelaskan; perubahan target, perintah, dampak atau langkah pemulihan memerlukan persetujuan baru. Diam atau jawaban ambigu bukan persetujuan.

Termasuk berisiko: registrasi/penghapusan/ganti SN ONU; perubahan VLAN, WAN, port, profile, bandwidth, ACS, Wi-Fi, routing dan akses management; shutdown/unlock/aktivasi PON; DHCP renew; reboot/factory reset/reset-card/swap; perubahan akun/password/SSH/Telnet/SNMP/waktu; penonaktifan proteksi; pembukaan akses remote; serta `write` atau penyimpanan permanen. Rollback yang mengubah perangkat juga harus tercakup izin atau dimintakan izin baru.

Pembacaan status biasa pada target yang sudah diotorisasi dapat dilakukan tanpa izin mutasi tambahan. Jika tingkat risiko tidak jelas, berhenti dan tanyakan. Jangan melanjutkan mutasi otomatis setelah error, timeout atau putus koneksi: periksa kondisi secara baca-saja, lalu minta persetujuan baru bila tindakan lanjutan diperlukan. Dalam proses tanpa pengguna hadir, jangan lakukan tindakan berisiko tanpa persetujuan spesifik yang sudah tercatat.

## Kapan Digunakan
Operator meminta akses manajemen web ONT dari jaringan manajemen. Jangan dipicu otomatis saat provisioning PPPoE.

## Prosedur
1. Tentukan IP WAN dari `show gpon remote-onu ip-host <ONU_IF>`, subnet admin yang diizinkan, dan durasi akses.
2. Perintah sumber membuka web/HTTP port 80. HTTP tidak mengenkripsi login. Prioritaskan VPN/jaringan manajemen terisolasi dan HTTPS jika perangkat mendukungnya. Jangan membuka antarmuka ini ke seluruh Internet.
3. Pastikan ACL/firewall pembatas sumber sudah diterapkan dan diuji. Sintaks ACL serta penonaktifan tidak tersedia di sumber; konfirmasi lewat manual firmware sebelum perubahan. Jangan mengarang command rollback.
4. Setelah rencana penutupan dan persetujuan eksplisit tersedia:
```text
configure terminal
pon-onu-mng <ONU_IF>
security-mgmt <RULE_ID> state enable mode forward protocol web
exit
end
```
`212` pada sumber adalah contoh ID rule, bukan port TCP. Gunakan ID yang sesuai firmware dan tidak bentrok.
5. Akhiri akses setelah pekerjaan selesai dengan prosedur penutupan yang telah diverifikasi; jangan membiarkan akses sementara menjadi permanen.

## Pitfalls
IP WAN yang terisi tidak membuktikan web dapat diakses. Jangan menonaktifkan firewall atau menyebarkan kredensial untuk mengatasi kegagalan akses. Jangan menyebut HTTPS tersedia bila belum diverifikasi.

## Verifikasi
Uji akses dari sumber admin yang diizinkan serta penolakan dari sumber lain. Sesudah penutupan, buktikan akses sementara sudah tidak tersedia. Catat rule, target, dan waktu tanpa password.

## Prasyarat dan pengaman

Target C320; kompatibilitas C300 wajib dikonfirmasi lewat dokumentasi firmware atau bantuan `?`. Perintah berikut adalah template CLI OLT, bukan perintah shell OS. Gunakan sesi perangkat yang telah diotorisasi atau minta operator menjalankannya; tidak ada koneksi otomatis dalam paket ini.

Validasi identitas OLT, port, SN, ONU ID, VLAN, nama profile, dan seluruh placeholder sebelum penggunaan. VLAN 1–4094; ID dan port harus tersedia serta sesuai kapasitas perangkat. Tolak input berisi newline atau pemisah perintah. Jangan menyalin alamat, serial, password, atau angka contoh sebagai konfigurasi produksi.

Sebelum perubahan: simpan konfigurasi awal, petakan dampak, tentukan rencana pemulihan, dan minta persetujuan target serta perubahan spesifik. Kerjakan satu target dahulu. Berhenti jika command ditolak; jangan mencoba variasi mutasi secara acak. Jangan menyimpan perubahan permanen sebelum verifikasi layanan dan izin penyimpanan. Password diisi operator melalui jalur aman; jangan dicetak ke laporan atau log.

## Sumber

Randy Filan (randifilan), zte-c320; adaptasi prosedural. Lisensi sumber belum diverifikasi; tidak diberi lisensi baru.
https://github.com/randifilan/zte-c320/tree/bee34b4794055c7c67c32216c471cbb675342ca7
