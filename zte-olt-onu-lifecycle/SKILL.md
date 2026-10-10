---
name: zte-olt-onu-lifecycle
description: Reboot dan reset ONT ZTE dengan pengaman operasi.
version: 0.1.0
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [zte, olt, onu, reboot, factory-reset]
    related_skills: [zte-olt-onu-diagnostics, zte-olt-onu-provisioning]
---
# Lifecycle ONT ZTE

Menangani reboot dan factory reset ONT. Semua operasi disruptif; factory reset berpotensi menghapus konfigurasi dan memutus layanan permanen sampai reprovisioning.

## Persetujuan pengguna untuk eksekusi berisiko

Wajib minta dan tunggu persetujuan eksplisit pengguna sebelum setiap eksekusi berisiko. Permintaan diagnosis, aktivasi umum, pembuatan skill, atau persetujuan sebelumnya bukan izin untuk tindakan baru.

Sebelum meminta izin, tampilkan target pelanggan/SN/interface/slot, perintah atau kelompok perubahan yang tepat (rahasia disamarkan), dampak layanan/keamanan, potensi kehilangan konfigurasi, dan rencana pemulihan. Eksekusi hanya tindakan dalam lingkup yang disetujui. Pengguna boleh menyetujui satu kelompok perintah yang sudah dijelaskan; perubahan target, perintah, dampak atau langkah pemulihan memerlukan persetujuan baru. Diam atau jawaban ambigu bukan persetujuan.

Termasuk berisiko: registrasi/penghapusan/ganti SN ONU; perubahan VLAN, WAN, port, profile, bandwidth, ACS, Wi-Fi, routing dan akses management; shutdown/unlock/aktivasi PON; DHCP renew; reboot/factory reset/reset-card/swap; perubahan akun/password/SSH/Telnet/SNMP/waktu; penonaktifan proteksi; pembukaan akses remote; serta `write` atau penyimpanan permanen. Rollback yang mengubah perangkat juga harus tercakup izin atau dimintakan izin baru.

Pembacaan status biasa pada target yang sudah diotorisasi dapat dilakukan tanpa izin mutasi tambahan. Jika tingkat risiko tidak jelas, berhenti dan tanyakan. Jangan melanjutkan mutasi otomatis setelah error, timeout atau putus koneksi: periksa kondisi secara baca-saja, lalu minta persetujuan baru bila tindakan lanjutan diperlukan. Dalam proses tanpa pengguna hadir, jangan lakukan tindakan berisiko tanpa persetujuan spesifik yang sudah tercatat.

## Kapan Digunakan

- Reboot ONT sudah disetujui untuk pemulihan gangguan.
- Factory reset diminta eksplisit dan konfigurasi pemulihan tersedia.
- Jangan gunakan sebagai langkah diagnosis pertama.

## Pemeriksaan Wajib

1. Verifikasi `<ONU_IF>`, serial, pelanggan, dan layanan.
2. Simpan output berikut:
   ```text
   show gpon onu detail-info <ONU_IF>
   show run interface <ONU_IF>
   show onu running config <ONU_IF>
   ```
3. Nyatakan dampak dan minta persetujuan eksplisit untuk operasi spesifik.
4. Untuk factory reset, pastikan backup konfigurasi dan prosedur reprovisioning tersedia.

## Reboot

```text
configure terminal
pon-onu-mng <ONU_IF>
reboot
```

Dampak: seluruh layanan ONT putus sementara.

## Factory Reset

```text
configure terminal
pon-onu-mng <ONU_IF>
restore factory
```

Dampak: konfigurasi ONT dapat terhapus. Jangan jalankan bila persetujuan hanya menyebut reboot.

## Pitfalls

- `reboot` dan `restore factory` bukan operasi setara.
- Jangan menebak target dari nama pelanggan; cocokkan serial.
- Jangan mengulang perintah karena prompt terlambat tanpa cek state baru.
- Sintaks dan dialog konfirmasi dapat berbeda menurut firmware.

## Verifikasi

Setelah reboot: cek state, detail-info, uptime, optik, dan layanan. Setelah factory reset: verifikasi ONT muncul sesuai kondisi yang diharapkan dan jalankan prosedur reprovisioning resmi; jangan improvisasi konfigurasi.

## Tambahan C320: mode CLI dan konfirmasi

Sumber kedua masuk langsung dari `configure terminal` ke `pon-onu-mng <ONU_IF>` tanpa `pon-onu`. Baris `pon-onu` pada sumber pertama ambigu dan bukan prasyarat universal, sehingga sengaja tidak dimasukkan ke template di atas. Tambahkan hanya jika firmware target terbukti memerlukannya; jangan menjalankan keduanya secara spekulatif.

Sumber C320 menampilkan `Confirm to reboot? [yes/no]:`. Jawab `yes` hanya setelah persetujuan reboot spesifik dan target cocok. Jangan mengulang reboot ketika koneksi terputus; periksa state melalui sesi operator yang tersedia.

## Prasyarat dan pengaman

Template ini adalah CLI perangkat, bukan shell OS. Tidak ada koneksi otomatis. Gunakan sesi operator berizin atau analisis output yang diberikan pengguna. Validasi OLT, interface, ID, dan firmware; tolak input yang menyisipkan newline/pemisah perintah. Jangan menjalankan placeholder literal. Redaksi password dan data pelanggan pada laporan.

Untuk perubahan, simpan kondisi awal, rencana pemulihan, dan persetujuan eksplisit target serta dampak. Tidak ada auto-save, retry mutasi, reset, atau penonaktifan proteksi sebagai langkah diagnosis. Jika tidak ada akses perangkat, keluarkan rencana saja dan tandai belum diuji. Sumber komunitas bukan jaminan sintaks untuk semua firmware C300/C320. Lisensi sumber belum diverifikasi; tidak diberikan lisensi ulang.
