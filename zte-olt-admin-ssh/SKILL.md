---
name: zte-olt-admin-ssh
description: Kelola akun admin dan akses SSH OLT ZTE.
version: 0.1.0
platforms: [linux, macos, windows]
---

# Akun Administrator dan SSH
## Persetujuan pengguna untuk eksekusi berisiko

Wajib minta dan tunggu persetujuan eksplisit pengguna sebelum setiap eksekusi berisiko. Permintaan diagnosis, aktivasi umum, pembuatan skill, atau persetujuan sebelumnya bukan izin untuk tindakan baru.

Sebelum meminta izin, tampilkan target pelanggan/SN/interface/slot, perintah atau kelompok perubahan yang tepat (rahasia disamarkan), dampak layanan/keamanan, potensi kehilangan konfigurasi, dan rencana pemulihan. Eksekusi hanya tindakan dalam lingkup yang disetujui. Pengguna boleh menyetujui satu kelompok perintah yang sudah dijelaskan; perubahan target, perintah, dampak atau langkah pemulihan memerlukan persetujuan baru. Diam atau jawaban ambigu bukan persetujuan.

Termasuk berisiko: registrasi/penghapusan/ganti SN ONU; perubahan VLAN, WAN, port, profile, bandwidth, ACS, Wi-Fi, routing dan akses management; shutdown/unlock/aktivasi PON; DHCP renew; reboot/factory reset/reset-card/swap; perubahan akun/password/SSH/Telnet/SNMP/waktu; penonaktifan proteksi; pembukaan akses remote; serta `write` atau penyimpanan permanen. Rollback yang mengubah perangkat juga harus tercakup izin atau dimintakan izin baru.

Pembacaan status biasa pada target yang sudah diotorisasi dapat dilakukan tanpa izin mutasi tambahan. Jika tingkat risiko tidak jelas, berhenti dan tanyakan. Jangan melanjutkan mutasi otomatis setelah error, timeout atau putus koneksi: periksa kondisi secara baca-saja, lalu minta persetujuan baru bila tindakan lanjutan diperlukan. Dalam proses tanpa pengguna hadir, jangan lakukan tindakan berisiko tanpa persetujuan spesifik yang sudah tercatat.

## Kapan Digunakan
Pembuatan/penggantian/penghapusan akun OLT atau konfigurasi SSH. Bukan akun PPPoE pelanggan.
## Prosedur
1. Rekam `show username`, `show ssh`, `show tcp brief` dengan redaksi secret/hash. TCP brief menunjukkan koneksi, bukan daftar identitas pengguna yang terjamin.
2. Pastikan console/out-of-band dan akun pemulihan berfungsi. Tentukan username, privilege minimal dan metode autentikasi. Jangan menghapus akun admin terakhir atau mengganti privilege tak sengaja.
3. Operator memasukkan secret melalui jalur aman. Dari global configuration, bentuk sumber untuk membuat atau mengganti password:
```text
service password-encryption
username <USERNAME> password <PASSWORD> privilege <PRIVILEGE>
```
Privilege 10/15 adalah contoh sumber, bukan default semua akun. `service password-encryption` tidak membuktikan penyimpanan kriptografi modern atau keamanan Telnet.
4. Konfigurasi SSH sumber, setelah dukungan firmware dan akses cadangan terkonfirmasi:
```text
ssh server enable
ssh server version 2
ssh server authentication mode local
ssh server authentication type pap
show ssh
```
Jangan menimpa integrasi AAA existing dengan local tanpa persetujuan. Verifikasi host key/fingerprint dan dukungan cipher lewat dokumentasi/operator; source tidak memberi command pembuatan key.
5. Untuk penghapusan akun yang disetujui: `no username <USERNAME>` pada global configuration. Uji akun pengganti terlebih dahulu melalui sesi kedua; sesi lama tetap terbuka sampai akses baru terbukti.
## Pitfalls
SSH aktif tidak otomatis mematikan Telnet. Sumber `no ssh server only` melonggarkan pembatasan SSH-only; jangan jalankan untuk setup SSH aman. Klaim batas 20 user dalam artikel tidak dijadikan batas universal firmware. Jangan mengetik rahasia melalui computer-use atau menyimpannya di file skill.
## Verifikasi
`show username`, `show ssh`; operator melakukan login baru dari management network dan memeriksa privilege. Jangan menutup sesi pemulihan sebelum lolos. Laporkan hasil tanpa hash/password.

## Pengaman
Template CLI perangkat, bukan shell OS. Validasi target/firmware dan input; tolak newline atau pemisah command. Rekam kondisi awal, rencana pemulihan, lalu minta persetujuan perubahan spesifik. Operator memasukkan rahasia melalui jalur aman; jangan meminta password/community di chat. Redaksi rahasia dari output. Jangan menyimpan permanen tanpa verifikasi dan izin. Sintaks C320 tidak dijamin untuk semua C300/model firmware.

## Sumber
Arianto, Tembolok.ID, artikel diperbarui 3 Maret 2026. Lisensi belum diverifikasi; tidak diberikan lisensi ulang.
https://www.tembolok.id/setting-olt-zte-c320-via-console-terminal-telnet/
