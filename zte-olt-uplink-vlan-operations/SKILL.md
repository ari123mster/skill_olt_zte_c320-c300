---
name: zte-olt-uplink-vlan-operations
description: Audit uplink dan VLAN serta operasi board OLT ZTE.
version: 0.1.0
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [zte, olt, uplink, vlan, switchover]
    related_skills: [zte-olt-system-health, zte-olt-vlan-provisioning]
---
# Uplink, VLAN, dan Operasi Board OLT ZTE

Membaca optik uplink dan membership VLAN. Juga mendokumentasikan reset slot dan switchover sebagai operasi berisiko tinggi.

## Persetujuan pengguna untuk eksekusi berisiko

Wajib minta dan tunggu persetujuan eksplisit pengguna sebelum setiap eksekusi berisiko. Permintaan diagnosis, aktivasi umum, pembuatan skill, atau persetujuan sebelumnya bukan izin untuk tindakan baru.

Sebelum meminta izin, tampilkan target pelanggan/SN/interface/slot, perintah atau kelompok perubahan yang tepat (rahasia disamarkan), dampak layanan/keamanan, potensi kehilangan konfigurasi, dan rencana pemulihan. Eksekusi hanya tindakan dalam lingkup yang disetujui. Pengguna boleh menyetujui satu kelompok perintah yang sudah dijelaskan; perubahan target, perintah, dampak atau langkah pemulihan memerlukan persetujuan baru. Diam atau jawaban ambigu bukan persetujuan.

Termasuk berisiko: registrasi/penghapusan/ganti SN ONU; perubahan VLAN, WAN, port, profile, bandwidth, ACS, Wi-Fi, routing dan akses management; shutdown/unlock/aktivasi PON; DHCP renew; reboot/factory reset/reset-card/swap; perubahan akun/password/SSH/Telnet/SNMP/waktu; penonaktifan proteksi; pembukaan akses remote; serta `write` atau penyimpanan permanen. Rollback yang mengubah perangkat juga harus tercakup izin atau dimintakan izin baru.

Pembacaan status biasa pada target yang sudah diotorisasi dapat dilakukan tanpa izin mutasi tambahan. Jika tingkat risiko tidak jelas, berhenti dan tanyakan. Jangan melanjutkan mutasi otomatis setelah error, timeout atau putus koneksi: periksa kondisi secara baca-saja, lalu minta persetujuan baru bila tindakan lanjutan diperlukan. Dalam proses tanpa pengguna hadir, jangan lakukan tindakan berisiko tanpa persetujuan spesifik yang sudah tercatat.

## Kapan Digunakan

- Audit power optik uplink atau anggota VLAN.
- Investigasi uplink sebelum eskalasi.
- Reset card atau switchover hanya atas change approval eksplisit.

## Pemeriksaan Baca-Saja

Optik uplink:
```text
show interface optical-module-info <XGEI_IF>
```
Catat vendor/module, wavelength, RxPower, TxPower, bias, suhu, voltage, dan threshold yang ditampilkan perangkat. Periksa counter/error interface dengan command firmware setempat; sumber hanya mengingatkan CRC tetapi tidak memberi command-nya.

Ringkasan VLAN:
```text
show vlan summary
```

Detail VLAN:
```text
show vlan <VLAN_ID>
```
Catat tagged/untagged membership, TPID, multicast behavior, dan interface terkait.

## Reset Slot

```text
reset-card slotno <SLOT>
```

Risiko: layanan pada seluruh card/slot dapat putus. Sebelum menjalankan:
1. Verifikasi slot lewat `show card` dan `show card slotno <SLOT>`.
2. Petakan pelanggan/uplink terdampak.
3. Pastikan redundancy dan rollback/escalation plan.
4. Minta persetujuan eksplisit yang menyebut slot.

## Switchover Control Module

```text
swap
```

Risiko: pergantian control module dapat mengganggu control plane. Jangan gunakan sebagai percobaan umum. Sebelum menjalankan, verifikasi active/standby sehat, sinkronisasi sesuai SOP vendor, akses out-of-band, dan change approval.

## Pitfalls

- Jangan membandingkan Rx/Tx dengan threshold contoh; gunakan threshold yang tampil pada perangkat dan desain link.
- Membership VLAN salah satu interface tidak membuktikan forwarding end-to-end.
- `reset-card` dan `swap` berdampak luas; jangan jalankan dari diagnosis tunggal.
- Sintaks singkat `sho` di sumber diganti `show` agar jelas.

## Verifikasi

Setelah operasi berisiko, cek `show card`, health system, uplink, VLAN, alarm, dan layanan terdampak. Catat kondisi sebelum/sesudah serta siapa yang menyetujui.

## Prasyarat dan pengaman

Template ini adalah CLI perangkat, bukan shell OS. Tidak ada koneksi otomatis. Gunakan sesi operator berizin atau analisis output yang diberikan pengguna. Validasi OLT, interface, ID, dan firmware; tolak input yang menyisipkan newline/pemisah perintah. Jangan menjalankan placeholder literal. Redaksi password dan data pelanggan pada laporan.

Untuk perubahan, simpan kondisi awal, rencana pemulihan, dan persetujuan eksplisit target serta dampak. Tidak ada auto-save, retry mutasi, reset, atau penonaktifan proteksi sebagai langkah diagnosis. Jika tidak ada akses perangkat, keluarkan rencana saja dan tandai belum diuji. Sumber komunitas bukan jaminan sintaks untuk semua firmware C300/C320. Lisensi sumber belum diverifikasi; tidak diberikan lisensi ulang.

## Tambahan Tembolok: status fisik uplink
```text
show interface port-status <UPLINK_IF>
show run interface <UPLINK_IF>
```
Catat link/admin status, media, native VLAN, speed, duplex dan negotiation. Artikel berisi ketidaksesuaian: perintah negotiation auto tetapi output no negotiation auto, serta label GE/FE yang tidak konsisten. Gunakan spesifikasi card/SFP dan hasil aktual; jangan memaksa auto-negotiation atau speed dari contoh. Flowcontrol/isolation bukan parameter yang boleh dimatikan otomatis.
