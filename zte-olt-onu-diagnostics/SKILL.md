---
name: zte-olt-onu-diagnostics
description: Diagnosis status dan kualitas ONT ZTE C300/C320.
version: 0.1.0
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [zte, olt, onu, gpon, diagnostics]
    related_skills: []
---

# Diagnosis ONT ZTE C300/C320

Gunakan perintah baca-saja untuk menilai status, sinyal, trafik, identitas, dan histori ONT. Jangan menyimpulkan akar masalah dari satu indikator.

## Kapan Digunakan

- ONT offline, LOS, lambat, flapping, atau identitas perangkat perlu dicek.
- Perlu MAC pelanggan, versi ONT, uptime, jarak, atau utilisasi saat ini.
- Jangan gunakan untuk mengubah konfigurasi, reboot, reset, atau lock port.

## Input Wajib

- `<OLT_IF>`, contoh `gpon-olt_1/2/5`.
- `<ONU_ID>`, contoh `5`.
- `<ONU_IF>`, contoh `gpon-onu_1/2/5:5`.

Pastikan ketiganya menunjuk ONT sama sebelum menyusun perintah.

## Prosedur

1. Cek state:
   ```text
   show gpon onu state <OLT_IF> <ONU_ID>
   ```
   Normal pada contoh sumber: `Admin enable`, `OMCC enable`, `O7 operation`, `Phase working`. `LOS` atau `OMCC disable` menunjukkan gangguan, bukan otomatis penyebab final.

2. Cek optik:
   ```text
   show pon power attenuation <ONU_IF>
   ```
   Catat upstream Rx/Tx, downstream Tx/Rx, dan attenuation. `no signal` atau `N/A` konsisten dengan jalur putus/offline. Nilai batas aman harus mengikuti desain optik dan spesifikasi operator; jangan karang threshold universal.

3. Cek trafik real-time:
   ```text
   show interface <ONU_IF>
   ```
   Catat input/output Bps, pps, dan throughput. Snapshot tunggal bukan bukti congestion; ulangi sesuai interval operasional.

4. Cek detail dan histori:
   ```text
   show gpon onu detail-info <ONU_IF>
   ```
   Ambil state, serial, distance, online duration, serta riwayat offline. `LOS` mengarah ke masalah fisik/sinyal; `DyingGasp` biasanya ONT kehilangan daya. Tetap korelasikan dengan alarm dan kondisi lapangan.

5. Cek MAC:
   ```text
   show mac gpon onu <ONU_IF>
   ```
   Laporkan MAC, VLAN, dan vport tanpa mengubah tabel.

6. Cek versi/perangkat:
   ```text
   show gpon remote-onu equip <ONU_IF>
   ```
   Catat Vendor ID, Version, EquipID, Model, SN, dan OperState.

## Format Hasil

```text
Target: <ONU_IF>
State: <admin>/<omcc>/<o7>/<phase>
Optik: up Rx <...>, down Rx <...>, attenuation <...>
Trafik: input <...>, output <...>
Uptime/jarak: <...>/<...>
Gangguan terakhir: <cause dan waktu>
MAC/VLAN: <...>
Model/versi: <...>
Kesimpulan: <fakta teramati>
Langkah berikut: <cek aman berikutnya>
```

## Pitfalls

- Singkatan `sho` dapat tersedia, tetapi gunakan bentuk penuh `show` agar jelas.
- Output dan field dapat berbeda menurut firmware C300/C320.
- Jangan menyamakan `Admin status: unlock` dengan `Operate status: enable`.
- Jangan menyebut kualitas optik baik/buruk tanpa threshold operator.

## Verifikasi

Target pada semua output harus sama. Kesimpulan wajib menyebut bukti output, bukan tebakan.

## Tambahan C320: cakupan state dan model

Gunakan cakupan terkecil yang menjawab masalah. Baca-saja:
```text
show gpon onu uncfg
show gpon onu state
show gpon onu state <OLT_IF>
show gpon remote-onu model <ONU_IF>
```
`uncfg` menampilkan ONU belum terdaftar, bukan ID registrasi final. State tanpa interface mencakup semua PON; jangan menganggap satu halaman sebagai seluruh hasil bila output terpotong. `model` melengkapi `equip`; cocokkan Equipment ID dan model, jangan menyimpulkan jumlah port hanya dari nama.

Trafik `Bps` berarti byte per detik, bukan bit per detik; konversi ke bit/s dengan faktor 8. `pps` adalah paket per detik. Pembulatan throughput 0.0% tidak berarti tidak ada trafik. Attenuation dalam dB berbeda dari power dBm. Nol pada System uptime/kolom histori dapat merupakan field kosong atau tidak didukung; tidak membuktikan baru reboot. `0000-00-00` bukan waktu kejadian yang valid.

Sumber tambahan: https://github.com/randifilan/zte-c320/tree/bee34b4794055c7c67c32216c471cbb675342ca7

## Batas penggunaan

Template ini adalah CLI perangkat, bukan shell OS. Tidak ada koneksi otomatis. Gunakan sesi operator berizin atau analisis output yang diberikan pengguna. Validasi OLT, interface, ID, dan firmware; tolak input yang menyisipkan newline/pemisah perintah. Jangan menjalankan placeholder literal. Redaksi password dan data pelanggan pada laporan.

Untuk perubahan, simpan kondisi awal, rencana pemulihan, dan persetujuan eksplisit target serta dampak. Tidak ada auto-save, retry mutasi, reset, atau penonaktifan proteksi sebagai langkah diagnosis. Jika tidak ada akses perangkat, keluarkan rencana saja dan tandai belum diuji. Sumber komunitas bukan jaminan sintaks untuk semua firmware C300/C320. Lisensi sumber belum diverifikasi; tidak diberikan lisensi ulang.

## Sumber

Diadaptasi dari `00. Perintah Dasar OLT` oleh denniseptian:
https://github.com/denniseptian/ZTE-C300/blob/master/00.%20Perintah%20Dasar%20OLT
