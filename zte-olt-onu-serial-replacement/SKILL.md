---
name: zte-olt-onu-serial-replacement
description: Ganti serial ONU ZTE tanpa registrasi ulang sembarang.
version: 0.1.0
platforms: [linux, macos, windows]
---

# Penggantian Serial ONU

## Kapan Digunakan
Mengganti ONT rusak dengan perangkat pengganti pada interface ONU existing. Bukan registrasi pelanggan baru atau bypass otorisasi SN.

## Prasyarat
Target OLT, `<ONU_IF>`, SN lama dan baru, identitas pelanggan, model pengganti, izin pemilik jaringan, dan rencana pemulihan. Template adalah CLI OLT, bukan shell OS. Gunakan sesi operator berizin; tidak ada koneksi otomatis.

Validasi format interface dan SN menurut firmware. Tolak newline/pemisah perintah pada input. Jangan berasumsi model pengganti kompatibel dengan ONU-type lama. C300 memerlukan konfirmasi dukungan sintaks; sumber spesifik C320.

## Prosedur
1. Rekam konfigurasi dan identitas sebelum perubahan:
```text
show gpon onu detail-info <ONU_IF>
show run interface <ONU_IF>
show onu running config <ONU_IF>
show gpon onu by sn <OLD_SN>
show gpon onu by sn <NEW_SN>
show gpon onu uncfg
```
Pastikan SN baru tidak terikat pelanggan lain dan cocok label fisik. Jika ditemukan konflik, berhenti. Simpan snapshot terlindung; redaksi password pada laporan.
2. Cocokkan model, port, layanan, dan ONU-type. Jelaskan bahwa penggantian binding dapat memutus ONT lama dan layanan pelanggan. Minta persetujuan eksplisit atas interface, SN lama, dan SN baru.
3. Setelah persetujuan:
```text
configure terminal
interface <ONU_IF>
registration-method sn <NEW_SN>
exit
end
```
4. Jika gagal, jangan hapus/re-register ONU atau mengganti ONU-type secara otomatis. Evaluasi output; pengembalian binding ke `<OLD_SN>` memakai sintaks yang sama hanya atas persetujuan rollback dan jika perangkat lama memang hendak dipulihkan.

## Pitfalls
Mengganti serial bukan factory reset. Konfigurasi existing dapat tetap ada, tetapi kesesuaian layanan pada hardware baru harus diuji. Jangan menyalin SN contoh. Jangan melakukan batch replacement atau `write` sebelum hasil pilot dan izin persistensi.

## Verifikasi
Ulangi detail-info, pencarian SN baru, konfigurasi kedua lapisan, dan `show gpon onu state <OLT_IF> <ONU_ID>`. Serial harus sesuai target baru. Uji optik, MAC/VLAN, IP-host jika dipakai, dan layanan pelanggan. State working saja tidak cukup membuktikan layanan pulih. Laporkan hasil aktual; jika tidak terhubung ke OLT, tandai belum diuji perangkat.

## Sumber
Randy Filan, `07. Change ONU SN.md`:
https://github.com/randifilan/zte-c320/tree/bee34b4794055c7c67c32216c471cbb675342ca7/07.%20Change%20ONU%20SN.md
