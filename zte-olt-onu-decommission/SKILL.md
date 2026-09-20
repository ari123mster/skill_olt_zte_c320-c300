---
name: zte-olt-onu-decommission
description: Hapus registrasi ONU dengan verifikasi target.
version: 0.1.0
platforms: [linux, macos, windows]
---

# Penghapusan Registrasi ONU
## Persetujuan pengguna untuk eksekusi berisiko

Wajib minta dan tunggu persetujuan eksplisit pengguna sebelum setiap eksekusi berisiko. Permintaan diagnosis, aktivasi umum, pembuatan skill, atau persetujuan sebelumnya bukan izin untuk tindakan baru.

Sebelum meminta izin, tampilkan target pelanggan/SN/interface/slot, perintah atau kelompok perubahan yang tepat (rahasia disamarkan), dampak layanan/keamanan, potensi kehilangan konfigurasi, dan rencana pemulihan. Eksekusi hanya tindakan dalam lingkup yang disetujui. Pengguna boleh menyetujui satu kelompok perintah yang sudah dijelaskan; perubahan target, perintah, dampak atau langkah pemulihan memerlukan persetujuan baru. Diam atau jawaban ambigu bukan persetujuan.

Termasuk berisiko: registrasi/penghapusan/ganti SN ONU; perubahan VLAN, WAN, port, profile, bandwidth, ACS, Wi-Fi, routing dan akses management; shutdown/unlock/aktivasi PON; DHCP renew; reboot/factory reset/reset-card/swap; perubahan akun/password/SSH/Telnet/SNMP/waktu; penonaktifan proteksi; pembukaan akses remote; serta `write` atau penyimpanan permanen. Rollback yang mengubah perangkat juga harus tercakup izin atau dimintakan izin baru.

Pembacaan status biasa pada target yang sudah diotorisasi dapat dilakukan tanpa izin mutasi tambahan. Jika tingkat risiko tidak jelas, berhenti dan tanyakan. Jangan melanjutkan mutasi otomatis setelah error, timeout atau putus koneksi: periksa kondisi secara baca-saja, lalu minta persetujuan baru bila tindakan lanjutan diperlukan. Dalam proses tanpa pengguna hadir, jangan lakukan tindakan berisiko tanpa persetujuan spesifik yang sudah tercatat.

## Kapan Digunakan
Pelanggan berhenti atau ONU harus dihapus atas permintaan eksplisit. Jangan gunakan untuk ganti SN, reboot, atau diagnosis biasa.
## Prosedur
1. Konfirmasi OLT, pelanggan, SN, `<OLT_IF>`, `<ONU_ID>` dan `<ONU_IF>` cocok. Rekam detail-info, konfigurasi interface ONU dan ONU management, serta konfigurasi PON. Simpan backup terlindung dan rencana registrasi ulang bila pemulihan diperlukan.
2. Jelaskan penghapusan registrasi memutus semua layanan ONU dan dapat menghapus konfigurasi terkait. Minta konfirmasi eksplisit atas identitas target; tidak ada batch-delete default.
3. Setelah konfirmasi:
```text
configure terminal
interface <OLT_IF>
no onu <ONU_ID>
exit
end
```
4. Jangan menghapus VLAN/profile bersama atau mematikan PON. Registrasi ulang bukan undo otomatis; perlu konfigurasi cadangan dan izin terpisah.
## Pitfalls
Perintah berada pada interface gpon-olt, bukan gpon-onu. Hapus registrasi berbeda dari factory reset perangkat. ONU fisik mungkin kembali muncul di uncfg; itu bukan kegagalan penghapusan.
## Verifikasi
`show run interface <OLT_IF>`, `show gpon onu by sn <SERIAL_NUMBER>`, `show gpon onu uncfg <OLT_IF>`. Pastikan binding target terhapus dan pelanggan lain tidak berubah. Simpan via `write` hanya jika izin persistensi diberikan.

## Pengaman
Template CLI perangkat, bukan shell OS. Validasi target/firmware dan input; tolak newline atau pemisah command. Rekam kondisi awal, rencana pemulihan, lalu minta persetujuan perubahan spesifik. Operator memasukkan rahasia melalui jalur aman; jangan meminta password/community di chat. Redaksi rahasia dari output. Jangan menyimpan permanen tanpa verifikasi dan izin. Sintaks C320 tidak dijamin untuk semua C300/model firmware.

## Sumber
Arianto, Tembolok.ID, artikel diperbarui 3 Maret 2026. Lisensi belum diverifikasi; tidak diberikan lisensi ulang.
https://www.tembolok.id/setting-olt-zte-c320-via-console-terminal-telnet/
