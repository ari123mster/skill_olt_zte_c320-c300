---
name: zte-olt-onu-access-management
description: Kelola pencarian, port, dan IP-host ONT ZTE.
version: 0.1.0
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [zte, olt, onu, ethernet, ip-host]
    related_skills: []
---

# Akses dan Port ONT ZTE

Menemukan ONT berdasarkan SN, membaca IP-host/port Ethernet, serta menyiapkan perubahan lock, unlock, atau DHCP renew dengan pengaman.

## Persetujuan pengguna untuk eksekusi berisiko

Wajib minta dan tunggu persetujuan eksplisit pengguna sebelum setiap eksekusi berisiko. Permintaan diagnosis, aktivasi umum, pembuatan skill, atau persetujuan sebelumnya bukan izin untuk tindakan baru.

Sebelum meminta izin, tampilkan target pelanggan/SN/interface/slot, perintah atau kelompok perubahan yang tepat (rahasia disamarkan), dampak layanan/keamanan, potensi kehilangan konfigurasi, dan rencana pemulihan. Eksekusi hanya tindakan dalam lingkup yang disetujui. Pengguna boleh menyetujui satu kelompok perintah yang sudah dijelaskan; perubahan target, perintah, dampak atau langkah pemulihan memerlukan persetujuan baru. Diam atau jawaban ambigu bukan persetujuan.

Termasuk berisiko: registrasi/penghapusan/ganti SN ONU; perubahan VLAN, WAN, port, profile, bandwidth, ACS, Wi-Fi, routing dan akses management; shutdown/unlock/aktivasi PON; DHCP renew; reboot/factory reset/reset-card/swap; perubahan akun/password/SSH/Telnet/SNMP/waktu; penonaktifan proteksi; pembukaan akses remote; serta `write` atau penyimpanan permanen. Rollback yang mengubah perangkat juga harus tercakup izin atau dimintakan izin baru.

Pembacaan status biasa pada target yang sudah diotorisasi dapat dilakukan tanpa izin mutasi tambahan. Jika tingkat risiko tidak jelas, berhenti dan tanyakan. Jangan melanjutkan mutasi otomatis setelah error, timeout atau putus koneksi: periksa kondisi secara baca-saja, lalu minta persetujuan baru bila tindakan lanjutan diperlukan. Dalam proses tanpa pengguna hadir, jangan lakukan tindakan berisiko tanpa persetujuan spesifik yang sudah tercatat.

## Kapan Digunakan

- Lokasi ONT belum diketahui tetapi SN tersedia.
- Perlu memeriksa IP routing-mode atau status port Ethernet ONT.
- Perlu lock/unlock port atau renew DHCP client setelah persetujuan.

## Input Wajib

- SN untuk pencarian, atau `<ONU_IF>` yang sudah diverifikasi.
- `<ETH_IF>` untuk operasi port, contoh `eth_0/1`.
- ID IP-host, contoh `1`.

## Prosedur Baca-Saja

1. Cari ONT:
   ```text
   show gpon onu by sn <SERIAL_NUMBER>
   ```
   Simpan hasil `<ONU_IF>` dan cocokkan serial melalui detail-info sebelum mutasi.

2. Cek IP-host:
   ```text
   show gpon remote-onu ip-host <ONU_IF>
   ```
   Bedakan nilai konfigurasi `IP/Mask/Gateway` dari nilai aktif `CurIP/CurMask/CurGateway`.

3. Cek semua status port Ethernet:
   ```text
   show gpon remote-onu interface eth <ONU_IF>
   ```
   Bedakan `Admin status` dan `Operate status`.

## Operasi Perubahan

Sebelum menjalankan: tampilkan target ONT, serial, port/host ID, dampak, dan minta persetujuan eksplisit.

Masuk mode (sumber C320 kedua langsung memakai `pon-onu-mng`; baris `pon-onu` di sumber pertama ambigu, konfirmasi firmware sebelum memakainya):
```text
configure terminal
pon-onu
pon-onu-mng <ONU_IF>
```

Lock port:
```text
interface eth <ETH_IF> state lock
```

Unlock port:
```text
interface eth <ETH_IF> state unlock
```

Renew DHCP untuk IP-host:
```text
ip-host <HOST_ID> dhcp-enable false ping-response false traceroute-response false
ip-host <HOST_ID> dhcp-enable true ping-response true traceroute-response true
```

Renew memutus IP-host sementara. Jangan lakukan pada management path aktif tanpa jalur pemulihan.

## Pitfalls

- Hasil pencarian SN harus diverifikasi; jangan mutasi dari hasil search saja.
- Lock port memutus layanan di port tersebut.
- Toggle DHCP juga mengubah respons ping/traceroute sesuai contoh sumber.
- Satu ONT dapat memiliki beberapa IP-host dan beberapa port Ethernet.

## Verifikasi

Setelah perubahan, keluar ke mode privileged lalu ulangi perintah baca status port atau IP-host. Laporkan nilai sebelum dan sesudah.

## Tambahan C320: Wi-Fi dan IP-host

Untuk status radio baca:
```text
show gpon remote-onu interface wifi <ONU_IF>
```
Catat setiap `wifi_0/x`, admin/operate status, Tx/Rx rate, dan power beserta unit. Nilai nol bukan bukti radio rusak; dukungan laporan OMCI berbeda antar model.

Firmware C320 pada sumber kedua memakai `Current IP address`, `Current mask`, `Current gateway`, `Current primary DNS`, dan `Current second DNS`, bukan hanya `CurIP`. Host dapat memakai PPPoE, bukan selalu DHCP. Jangan men-toggle DHCP pada host PPPoE.

Sebelum renew, rekam flag DHCP, ping-response, dan traceroute-response aktual. Contoh pasangan false/true dari sumber mengubah ketiganya: jika flag awal ping/traceroute bukan true, jangan gunakan template itu mentah. Minta konfirmasi sintaks firmware yang mempertahankan kebijakan semula. Setelah selesai, pastikan flag final kembali ke kebijakan yang disetujui dan IP aktif diperoleh.


## Batas penggunaan

Template ini adalah CLI perangkat, bukan shell OS. Tidak ada koneksi otomatis. Gunakan sesi operator berizin atau analisis output yang diberikan pengguna. Validasi OLT, interface, ID, dan firmware; tolak input yang menyisipkan newline/pemisah perintah. Jangan menjalankan placeholder literal. Redaksi password dan data pelanggan pada laporan.

Untuk perubahan, simpan kondisi awal, rencana pemulihan, dan persetujuan eksplisit target serta dampak. Tidak ada auto-save, retry mutasi, reset, atau penonaktifan proteksi sebagai langkah diagnosis. Jika tidak ada akses perangkat, keluarkan rencana saja dan tandai belum diuji. Sumber komunitas bukan jaminan sintaks untuk semua firmware C300/C320. Lisensi sumber belum diverifikasi; tidak diberikan lisensi ulang.

