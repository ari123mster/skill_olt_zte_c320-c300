---
name: zte-olt-vlan-provisioning
description: Konfigurasi VLAN dan tagging uplink OLT ZTE.
version: 0.1.0
platforms: [linux, macos, windows]
---

# Provisioning VLAN dan Uplink

## Persetujuan pengguna untuk eksekusi berisiko

Wajib minta dan tunggu persetujuan eksplisit pengguna sebelum setiap eksekusi berisiko. Permintaan diagnosis, aktivasi umum, pembuatan skill, atau persetujuan sebelumnya bukan izin untuk tindakan baru.

Sebelum meminta izin, tampilkan target pelanggan/SN/interface/slot, perintah atau kelompok perubahan yang tepat (rahasia disamarkan), dampak layanan/keamanan, potensi kehilangan konfigurasi, dan rencana pemulihan. Eksekusi hanya tindakan dalam lingkup yang disetujui. Pengguna boleh menyetujui satu kelompok perintah yang sudah dijelaskan; perubahan target, perintah, dampak atau langkah pemulihan memerlukan persetujuan baru. Diam atau jawaban ambigu bukan persetujuan.

Termasuk berisiko: registrasi/penghapusan/ganti SN ONU; perubahan VLAN, WAN, port, profile, bandwidth, ACS, Wi-Fi, routing dan akses management; shutdown/unlock/aktivasi PON; DHCP renew; reboot/factory reset/reset-card/swap; perubahan akun/password/SSH/Telnet/SNMP/waktu; penonaktifan proteksi; pembukaan akses remote; serta `write` atau penyimpanan permanen. Rollback yang mengubah perangkat juga harus tercakup izin atau dimintakan izin baru.

Pembacaan status biasa pada target yang sudah diotorisasi dapat dilakukan tanpa izin mutasi tambahan. Jika tingkat risiko tidak jelas, berhenti dan tanyakan. Jangan melanjutkan mutasi otomatis setelah error, timeout atau putus koneksi: periksa kondisi secara baca-saja, lalu minta persetujuan baru bila tindakan lanjutan diperlukan. Dalam proses tanpa pengguna hadir, jangan lakukan tindakan berisiko tanpa persetujuan spesifik yang sudah tercatat.

## Kapan Digunakan
Membuat VLAN layanan atau tagging pada uplink. Untuk inspeksi saja gunakan audit uplink/VLAN.

## Prosedur
1. Catat VLAN existing dan membership dengan `show vlan summary`, `show vlan <VLAN_ID>`, serta konfigurasi uplink.
2. Konfirmasi VLAN yang harus lewat, media fisik, perangkat upstream, dan akses manajemen cadangan.
3. Buat satu VLAN, kembali ke global sebelum membuat VLAN lain:
```text
configure terminal
vlan <VLAN_ID>
name <VLAN_NAME>
exit
```
4. Tag hanya VLAN yang disetujui, bukan seluruh rentang contoh:
```text
interface <UPLINK_IF>
switchport mode hybrid
switchport vlan <VLAN_LIST> tag
end
```
5. `no shutdown` hanya bila aktivasi port disetujui. `hybrid-attribute copper` hanya untuk combo/media copper yang cocok; jangan untuk semua uplink optik.
6. Sumber mencantumkan `igmp version v2`, `igmp fast-leave enable`, `port-protect disable`, `uplink-isolate disable` di interface uplink. Ini opsi desain, bukan bagian wajib tagging. Jangan menonaktifkan isolasi/proteksi atau mengaktifkan fast-leave tanpa kajian topologi multicast dan keamanan.

## Pitfalls
Mengubah mode uplink dapat mengganggu VLAN existing. Fast-leave tidak cocok semua topologi downstream. VLAN management harus tetap dapat diakses. `!` pada contoh bukan pengganti perintah keluar mode.

## Verifikasi
Ulangi `show vlan summary`, `show vlan <VLAN_ID>` dan cek konfigurasi interface. Uji trafik layanan dan akses manajemen dari jalur nyata; konfigurasi tertulis bukan bukti konektivitas.

## Prasyarat dan pengaman

Target C320; kompatibilitas C300 wajib dikonfirmasi lewat dokumentasi firmware atau bantuan `?`. Perintah berikut adalah template CLI OLT, bukan perintah shell OS. Gunakan sesi perangkat yang telah diotorisasi atau minta operator menjalankannya; tidak ada koneksi otomatis dalam paket ini.

Validasi identitas OLT, port, SN, ONU ID, VLAN, nama profile, dan seluruh placeholder sebelum penggunaan. VLAN 1–4094; ID dan port harus tersedia serta sesuai kapasitas perangkat. Tolak input berisi newline atau pemisah perintah. Jangan menyalin alamat, serial, password, atau angka contoh sebagai konfigurasi produksi.

Sebelum perubahan: simpan konfigurasi awal, petakan dampak, tentukan rencana pemulihan, dan minta persetujuan target serta perubahan spesifik. Kerjakan satu target dahulu. Berhenti jika command ditolak; jangan mencoba variasi mutasi secara acak. Jangan menyimpan perubahan permanen sebelum verifikasi layanan dan izin penyimpanan. Password diisi operator melalui jalur aman; jangan dicetak ke laporan atau log.

## Sumber

Randy Filan (randifilan), zte-c320; adaptasi prosedural. Lisensi sumber belum diverifikasi; tidak diberi lisensi baru.
https://github.com/randifilan/zte-c320/tree/bee34b4794055c7c67c32216c471cbb675342ca7
