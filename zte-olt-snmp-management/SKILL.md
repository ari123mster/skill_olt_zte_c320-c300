---
name: zte-olt-snmp-management
description: Konfigurasi SNMP monitoring OLT secara terbatas.
version: 0.1.0
platforms: [linux, macos, windows]
---

# SNMP Monitoring
## Persetujuan pengguna untuk eksekusi berisiko

Wajib minta dan tunggu persetujuan eksplisit pengguna sebelum setiap eksekusi berisiko. Permintaan diagnosis, aktivasi umum, pembuatan skill, atau persetujuan sebelumnya bukan izin untuk tindakan baru.

Sebelum meminta izin, tampilkan target pelanggan/SN/interface/slot, perintah atau kelompok perubahan yang tepat (rahasia disamarkan), dampak layanan/keamanan, potensi kehilangan konfigurasi, dan rencana pemulihan. Eksekusi hanya tindakan dalam lingkup yang disetujui. Pengguna boleh menyetujui satu kelompok perintah yang sudah dijelaskan; perubahan target, perintah, dampak atau langkah pemulihan memerlukan persetujuan baru. Diam atau jawaban ambigu bukan persetujuan.

Termasuk berisiko: registrasi/penghapusan/ganti SN ONU; perubahan VLAN, WAN, port, profile, bandwidth, ACS, Wi-Fi, routing dan akses management; shutdown/unlock/aktivasi PON; DHCP renew; reboot/factory reset/reset-card/swap; perubahan akun/password/SSH/Telnet/SNMP/waktu; penonaktifan proteksi; pembukaan akses remote; serta `write` atau penyimpanan permanen. Rollback yang mengubah perangkat juga harus tercakup izin atau dimintakan izin baru.

Pembacaan status biasa pada target yang sudah diotorisasi dapat dilakukan tanpa izin mutasi tambahan. Jika tingkat risiko tidak jelas, berhenti dan tanyakan. Jangan melanjutkan mutasi otomatis setelah error, timeout atau putus koneksi: periksa kondisi secara baca-saja, lalu minta persetujuan baru bila tindakan lanjutan diperlukan. Dalam proses tanpa pengguna hadir, jangan lakukan tindakan berisiko tanpa persetujuan spesifik yang sudah tercatat.

## Kapan Digunakan
Integrasi NMS/monitoring atau NetNumen yang diotorisasi; SNMP bukan syarat aktivasi ONU.
## Prosedur
1. Konfirmasi NMS IP, ACL, versi SNMP, kebutuhan polling/trap, view dan izin RO/RW. Prioritaskan SNMPv3 jika didukung; sumber tidak menyediakan setup v3 lengkap sehingga jangan mengarangnya.
2. Sumber memberi SNMPv2c, community tidak terenkripsi. Gunakan hanya jaringan management terisolasi dengan ACL. Default desain RO, bukan RW. Operator mengisi secret:
```text
configure terminal
snmp-server community <COMMUNITY> view <VIEW> ro
snmp-server host <NMS_IP> version 2c <COMMUNITY> enable NOTIFICATIONS target-addr-name <TARGET_NAME>
exit
show snmp c
```
Trap host opsional bila diminta; IP NMS adalah penerima, bukan otomatis IP OLT. RW dapat memakai bentuk `snmp-server community <COMMUNITY> view <VIEW> rw` hanya dengan kebutuhan dan persetujuan khusus. Jangan otomatis memilih AllView bila view terbatas tersedia.
3. Penghapusan spesifik, hanya atas izin:
```text
configure terminal
no snmp-server community <COMMUNITY>
no snmp-server host target-addr-name <TARGET_NAME>
exit
```
## Pitfalls
Output `show snmp c` dapat membocorkan community; redaksi sebelum laporan. SNMP berguna untuk NMS selain NetNumen. Jangan menyalin community contoh atau membuka UDP management ke Internet. Penghapusan dapat menghentikan monitoring.
## Verifikasi
Operator menguji polling dari NMS berizin, penolakan sumber lain dan penerimaan trap jika diminta. Konfigurasi saja bukan bukti monitoring berjalan.

## Pengaman
Template CLI perangkat, bukan shell OS. Validasi target/firmware dan input; tolak newline atau pemisah command. Rekam kondisi awal, rencana pemulihan, lalu minta persetujuan perubahan spesifik. Operator memasukkan rahasia melalui jalur aman; jangan meminta password/community di chat. Redaksi rahasia dari output. Jangan menyimpan permanen tanpa verifikasi dan izin. Sintaks C320 tidak dijamin untuk semua C300/model firmware.

## Sumber
Arianto, Tembolok.ID, artikel diperbarui 3 Maret 2026. Lisensi belum diverifikasi; tidak diberikan lisensi ulang.
https://www.tembolok.id/setting-olt-zte-c320-via-console-terminal-telnet/
