---
name: zte-olt-onu-lifecycle
description: Reboot dan reset ONT ZTE dengan pengaman operasi.
version: 0.1.0
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [zte, olt, onu, reboot, factory-reset]
    related_skills: []
---

# Lifecycle ONT ZTE

Menangani reboot dan factory reset ONT. Semua operasi disruptif; factory reset berpotensi menghapus konfigurasi dan memutus layanan permanen sampai reprovisioning.

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
pon-onu
pon-onu-mng <ONU_IF>
reboot
```

Dampak: seluruh layanan ONT putus sementara.

## Factory Reset

```text
configure terminal
pon-onu
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

Sumber kedua masuk langsung dari `configure terminal` ke `pon-onu-mng <ONU_IF>` tanpa `pon-onu`. Baris `pon-onu` pada sumber pertama ambigu dan bukan prasyarat universal. Pilih sintaks mode yang dikonfirmasi firmware; jangan menjalankan keduanya secara spekulatif.

Sumber C320 menampilkan `Confirm to reboot? [yes/no]:`. Jawab `yes` hanya setelah persetujuan reboot spesifik dan target cocok. Jangan mengulang reboot ketika koneksi terputus; periksa state melalui sesi operator yang tersedia.

Sumber tambahan: https://github.com/randifilan/zte-c320/tree/bee34b4794055c7c67c32216c471cbb675342ca7

## Batas penggunaan

Template ini adalah CLI perangkat, bukan shell OS. Tidak ada koneksi otomatis. Gunakan sesi operator berizin atau analisis output yang diberikan pengguna. Validasi OLT, interface, ID, dan firmware; tolak input yang menyisipkan newline/pemisah perintah. Jangan menjalankan placeholder literal. Redaksi password dan data pelanggan pada laporan.

Untuk perubahan, simpan kondisi awal, rencana pemulihan, dan persetujuan eksplisit target serta dampak. Tidak ada auto-save, retry mutasi, reset, atau penonaktifan proteksi sebagai langkah diagnosis. Jika tidak ada akses perangkat, keluarkan rencana saja dan tandai belum diuji. Sumber komunitas bukan jaminan sintaks untuk semua firmware C300/C320. Lisensi sumber belum diverifikasi; tidak diberikan lisensi ulang.

## Sumber

Diadaptasi dari `00. Perintah Dasar OLT` oleh denniseptian:
https://github.com/denniseptian/ZTE-C300/blob/master/00.%20Perintah%20Dasar%20OLT
