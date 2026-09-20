---
name: zte-olt-onu-config-audit
description: Audit konfigurasi ONT dan layanan ZTE C300/C320.
version: 0.1.0
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [zte, olt, onu, gpon, configuration]
    related_skills: []
---

# Audit Konfigurasi ONT ZTE C300/C320

Membaca konfigurasi interface GPON dan manajemen ONU tanpa mengubah perangkat.

## Kapan Digunakan

- Audit VLAN, service-port, T-CONT, GEM port, flow, atau pemetaan port Ethernet.
- Membandingkan konfigurasi ONT dengan template layanan.
- Jangan gunakan untuk provisioning atau koreksi konfigurasi langsung.

## Input Wajib

- `<ONU_IF>`, contoh `gpon-onu_1/2/5:5`.
- Template layanan atau nilai yang diharapkan: VLAN, SVLAN, bandwidth profile, GEM, dan port.

## Prosedur

1. Ambil konfigurasi interface:
   ```text
   show run interface <ONU_IF>
   ```
   Pada firmware lain bentuk panjang dapat berupa:
   ```text
   show running-config interface <ONU_IF>
   ```

2. Ambil konfigurasi manajemen ONU:
   ```text
   show onu running config <ONU_IF>
   ```

3. Inventaris elemen berikut bila muncul:
   - `name` dan `description`
   - `tcont` dan profile
   - `gemport`, arah, serta traffic-limit
   - `switchport`, vport, VLAN, user-vlan, dan SVLAN
   - `service`, `flow`, `vlan-filter`, `ip-host`, dan mapping `eth_0/x`

4. Bandingkan dengan template. Pisahkan:
   - fakta aktual dari output;
   - nilai ekspektasi dari tiket/template;
   - mismatch yang perlu perubahan.

5. Berikan kandidat perubahan sebagai rencana saja. Jangan keluarkan perintah mutasi tanpa permintaan dan persetujuan eksplisit.

## Format Hasil

```text
Target: <ONU_IF>
T-CONT/profile: <...>
GEM/flow: <...>
VLAN/SVLAN: <...>
Port mapping: <...>
Traffic limit: <...>
Mismatch: <aktual> vs <ekspektasi>
Risiko perubahan: <...>
```

## Pitfalls

- `show run interface` dan `show onu running config` menampilkan lapisan berbeda; periksa keduanya.
- Jangan menganggap nama profile menunjukkan rate aktual tanpa melihat isi profile.
- Kesalahan satu digit VLAN atau ONU ID dapat berdampak ke pelanggan lain.
- Sintaks berbeda menurut firmware.

## Verifikasi

Semua VLAN, GEM, flow, dan port yang dilaporkan harus punya baris bukti dari output. Target harus cocok di kedua perintah.

## Tambahan C320: pencarian section dan pemetaan layanan

Alternatif baca dari sumber kedua:
```text
show run section | include <ONU_IF>
show run | begin interface <ONU_IF>
show run | begin pon-onu-mng <ONU_IF>
show run interface <OLT_IF>
```
Pipe di sini milik CLI OLT, bukan shell OS. `begin` dapat mencetak seluruh konfigurasi setelah titik cocok; batasi penanganan data pelanggan. `include` mungkin hanya mengembalikan baris cocok, bukan section utuh pada firmware lain. Jangan menilai baris tidak ditemukan sebagai konfigurasi tidak ada tanpa dua perintah audit utama.

Audit juga `sn-bind`, `registration-method`, `veip_1`, port Wi-Fi, native VLAN `def-vlan`, tagged list, service-port description, translasi user-vlan ke network VLAN, dan WAN profile. Redaksi password PPPoE sebelum membagikan konfigurasi.

Bentuk `show running-config interface` yang disebut di atas adalah kandidat umum, tidak terverifikasi dari dua sumber. Utamakan `show run interface`; jangan menganggap alternatif didukung sebelum memeriksa bantuan firmware.

Sumber tambahan: https://github.com/randifilan/zte-c320/tree/bee34b4794055c7c67c32216c471cbb675342ca7

## Batas penggunaan

Template ini adalah CLI perangkat, bukan shell OS. Tidak ada koneksi otomatis. Gunakan sesi operator berizin atau analisis output yang diberikan pengguna. Validasi OLT, interface, ID, dan firmware; tolak input yang menyisipkan newline/pemisah perintah. Jangan menjalankan placeholder literal. Redaksi password dan data pelanggan pada laporan.

Untuk perubahan, simpan kondisi awal, rencana pemulihan, dan persetujuan eksplisit target serta dampak. Tidak ada auto-save, retry mutasi, reset, atau penonaktifan proteksi sebagai langkah diagnosis. Jika tidak ada akses perangkat, keluarkan rencana saja dan tandai belum diuji. Sumber komunitas bukan jaminan sintaks untuk semua firmware C300/C320. Lisensi sumber belum diverifikasi; tidak diberikan lisensi ulang.

## Sumber

Diadaptasi dari `00. Perintah Dasar OLT` oleh denniseptian:
https://github.com/denniseptian/ZTE-C300/blob/master/00.%20Perintah%20Dasar%20OLT
