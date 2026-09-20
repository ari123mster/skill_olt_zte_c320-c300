---
name: zte-olt-system-health
description: Periksa kesehatan sistem dan board OLT ZTE.
version: 0.1.0
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [zte, olt, board, cpu, temperature]
    related_skills: []
---

# Kesehatan Sistem OLT ZTE

Mengumpulkan uptime, inventaris board, CPU, memori, suhu, dan detail slot secara baca-saja.

## Kapan Digunakan

- Health check OLT, anomali resource, board, atau suhu.
- Perlu status control module, GPON board, dan uplink module.
- Jangan gunakan untuk reset card atau switchover.

## Prosedur

1. Uptime dan versi sistem:
   ```text
   show system-group
   ```

2. Inventaris/status board:
   ```text
   show card
   ```
   Catat slot, configured type, real type, port, versi, serta `INSERVICE`/`STANDBY`.

3. CPU dan memori:
   ```text
   show processor
   ```
   Bandingkan CPU 5s/1m/5m. Lonjakan 5s tanpa kenaikan 1m/5m belum cukup membuktikan masalah menetap.

4. Suhu:
   ```text
   show temperature
   ```
   Gunakan threshold perangkat/operator, bukan angka universal.

5. Detail slot:
   ```text
   show card slotno <SLOT>
   ```
   Catat status, real type, serial, port count, versi, resource, threshold, dan uptime.

## Interpretasi

- `GTGOE`: contoh sumber menyebut board 8 port.
- `GTGH`: contoh sumber menyebut board 16 port.
- `SCXN`: contoh menunjukkan control module aktif/standby.
- `HUTQ`: contoh menunjukkan uplink module.

Identifikasi ini bersifat contoh firmware/hardware; verifikasi terhadap inventaris perangkat aktual.

## Format Hasil

```text
Sistem/uptime: <...>
Board tidak INSERVICE: <...>
Control aktif/standby: <...>
CPU tinggi: <slot dan window>
Memori tinggi: <slot dan persen>
Suhu/threshold: <...>
Slot detail: <...>
```

## Pitfalls

- Output uptime yang tidak masuk akal dapat menandakan bug counter/firmware; jangan langsung dipercaya.
- `N/A` suhu pada slot tertentu belum tentu fault bila sensor tidak tersedia.
- Jangan reset board hanya dari satu snapshot CPU.

## Verifikasi

Semua slot bermasalah harus dirujuk ke baris `show card` dan, bila relevan, `show card slotno`. Catat timestamp pengambilan data.

## Tambahan C320: inventaris berbeda

Sumber kedua menunjukkan GTGH/GTGHG 16 port dan SMXA pada slot 3/4, berbeda dari SCXN/HUTQ pada contoh C300. `OFFLINE` pada slot yang dikonfigurasi harus dibandingkan dengan inventaris fisik dan desain redundansi; tidak otomatis berarti board rusak atau standby sehat. Field sistem juga meliputi system name, location, contact, dan versi C320; redaksi kontak saat berbagi laporan.

Sumber tambahan: https://github.com/randifilan/zte-c320/tree/bee34b4794055c7c67c32216c471cbb675342ca7

## Batas penggunaan

Template ini adalah CLI perangkat, bukan shell OS. Tidak ada koneksi otomatis. Gunakan sesi operator berizin atau analisis output yang diberikan pengguna. Validasi OLT, interface, ID, dan firmware; tolak input yang menyisipkan newline/pemisah perintah. Jangan menjalankan placeholder literal. Redaksi password dan data pelanggan pada laporan.

Untuk perubahan, simpan kondisi awal, rencana pemulihan, dan persetujuan eksplisit target serta dampak. Tidak ada auto-save, retry mutasi, reset, atau penonaktifan proteksi sebagai langkah diagnosis. Jika tidak ada akses perangkat, keluarkan rencana saja dan tandai belum diuji. Sumber komunitas bukan jaminan sintaks untuk semua firmware C300/C320. Lisensi sumber belum diverifikasi; tidak diberikan lisensi ulang.

## Sumber

Diadaptasi dari `00. Perintah Dasar OLT` oleh denniseptian:
https://github.com/denniseptian/ZTE-C300/blob/master/00.%20Perintah%20Dasar%20OLT
