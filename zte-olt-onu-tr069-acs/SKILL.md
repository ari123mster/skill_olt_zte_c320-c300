---
name: zte-olt-onu-tr069-acs
description: Tambahkan TR-069 dan ACS saat aktivasi ONU ZTE.
version: 0.1.0
platforms: [linux, macos, windows]
---

# Aktivasi Opsional TR-069/ACS

## Persetujuan pengguna untuk eksekusi berisiko

Wajib minta dan tunggu persetujuan eksplisit pengguna sebelum setiap eksekusi berisiko. Permintaan diagnosis, aktivasi umum, pembuatan skill, atau persetujuan sebelumnya bukan izin untuk tindakan baru.

Sebelum meminta izin, tampilkan target pelanggan/SN/interface/slot, perintah atau kelompok perubahan yang tepat (rahasia disamarkan), dampak layanan/keamanan, potensi kehilangan konfigurasi, dan rencana pemulihan. Eksekusi hanya tindakan dalam lingkup yang disetujui. Pengguna boleh menyetujui satu kelompok perintah yang sudah dijelaskan; perubahan target, perintah, dampak atau langkah pemulihan memerlukan persetujuan baru. Diam atau jawaban ambigu bukan persetujuan.

Termasuk berisiko: registrasi/penghapusan/ganti SN ONU; perubahan VLAN, WAN, port, profile, bandwidth, ACS, Wi-Fi, routing dan akses management; shutdown/unlock/aktivasi PON; DHCP renew; reboot/factory reset/reset-card/swap; perubahan akun/password/SSH/Telnet/SNMP/waktu; penonaktifan proteksi; pembukaan akses remote; serta `write` atau penyimpanan permanen. Rollback yang mengubah perangkat juga harus tercakup izin atau dimintakan izin baru.

Pembacaan status biasa pada target yang sudah diotorisasi dapat dilakukan tanpa izin mutasi tambahan. Jika tingkat risiko tidak jelas, berhenti dan tanyakan. Jangan melanjutkan mutasi otomatis setelah error, timeout atau putus koneksi: periksa kondisi secara baca-saja, lalu minta persetujuan baru bila tindakan lanjutan diperlukan. Dalam proses tanpa pengguna hadir, jangan lakukan tindakan berisiko tanpa persetujuan spesifik yang sudah tercatat.

## Kapan Digunakan
Pengguna menyetujui tambahan TR-069/ACS pada aktivasi PPPoE atau bridge, atau meminta ACS untuk ONU existing. Jangan aktifkan otomatis. Sumber adalah contoh komunitas, bukan jaminan dukungan semua C300/C320 atau ONT.

## Klarifikasi wajib

Setelah mode PPPoE/bridge jelas, tanyakan: "Mau ditambah TR-069/ACS atau tidak?" Tunggu jawaban sebelum menyusun konfigurasi final. Jika sudah dijawab eksplisit, jangan bertanya ulang. Jawaban tidak berarti lewati seluruh perubahan ACS; untuk ONU existing jangan menghapus ACS lama tanpa permintaan terpisah.

Jika ya, lengkapi:
- Identitas pelanggan, OLT/PON, ONU interface, SN, model dan firmware.
- URL ACS beserta scheme, port dan path; konfirmasi server dikelola pihak yang diizinkan.
- Jalur management: VLAN khusus atau WAN existing. Sumber hanya memberi contoh VLAN khusus dengan WAN DHCP; jangan mengarang template WAN existing.
- Customer/network VLAN, priority, VLAN profile, GEM/vport, service-port ID, WAN ID dan TR-069 management ID yang tersedia.
- DHCP, DNS bila URL menggunakan hostname, route dan ACL ke ACS; bandwidth/profile layanan tetap sesuai paket pelanggan.
- Metode autentikasi dan akun ACS melalui jalur aman. Jangan meminta password di chat atau mencetaknya dalam log/ringkasan. Autentikasi ACS berbeda dari akun PPPoE dan connection-request; sumber tidak menyediakan konfigurasi connection-request.

Tampilkan ringkasan PPPoE/bridge + TR-069 ya/tidak, target, VLAN/WAN, URL ACS tanpa rahasia, dampak dan rencana pemulihan. Minta persetujuan eksplisit sebelum mutasi. Tanpa jawaban/data lengkap, berhenti.

## Prasyarat dan pengaman

Baca konfigurasi sebelum perubahan melalui `show run interface <ONU_IF>` dan `show onu running config <ONU_IF>`. Redaksi password. Validasi semua ID tidak bentrok, format interface/SN, VLAN 1–4094, priority 0–7 dan URL tanpa newline/pemisah perintah. Semua blok adalah CLI OLT, bukan shell OS; gunakan sesi operator berizin, tanpa koneksi otomatis.

ACS dapat mengubah konfigurasi ONT dari jauh. Gunakan server tepercaya, kredensial unik, ACL jaringan manajemen, dan HTTPS bila firmware mendukungnya. Contoh sumber memakai HTTP dengan basic authentication; jangan menganggap aman untuk Internet publik. HTTP tidak mengenkripsi kredensial. Jika hanya HTTP didukung, perlukan jaringan manajemen terisolasi dan persetujuan risiko; jangan menyalin akun default sumber.

## Prosedur

1. Selesaikan pemilihan mode layanan utama. Bridge tidak berarti membuat PPPoE di ONT; ACS merupakan jalur manajemen terpisah. Dukungan bridge + management WAN harus diverifikasi pada model/firmware aktual.
2. Pastikan ACS VLAN melewati uplink dan tersedia DHCP/routing menuju ACS. Buat profile VLAN yang sesuai melalui prosedur profile GPON, bukan mengasumsikan profile bernama TR069 sudah ada.
3. Setelah persetujuan, tambahkan mapping ke GEM/vport yang sudah diverifikasi, tanpa menimpa layanan lain:
```text
configure terminal
interface <ONU_IF>
service-port <ACS_SERVICE_PORT_ID> vport <ACS_VPORT_ID> user-vlan <ACS_CUSTOMER_VLAN> vlan <ACS_NETWORK_VLAN>
service-port <ACS_SERVICE_PORT_ID> description ACS
exit
pon-onu-mng <ONU_IF>
service <ACS_SERVICE_NAME> gemport <ACS_GEM_ID> vlan <ACS_CUSTOMER_VLAN>
wan-ip <ACS_WAN_ID> mode DHCP vlan-profile <ACS_VLAN_PROFILE>
tr069-mgmt <TR069_ID> state unlock
tr069-mgmt <TR069_ID> acs <ACS_URL> validate basic username <ACS_USERNAME> password <ACS_PASSWORD>
tr069-mgmt <TR069_ID> tag pri <PRIORITY> vlan <ACS_CUSTOMER_VLAN>
exit
end
```
Template diparameterkan dari sumber; konfirmasi grammar, ID dan metode autentikasi di firmware. Operator mengisi rahasia melalui jalur aman. Jangan menambahkan parameter host atau binding WAN yang tidak ada di sumber tanpa bukti dokumentasi.
4. Jangan mengubah T-CONT menjadi profile 1G atau traffic-limit default hanya karena contoh memakainya. Jangan menambahkan VLAN PPPoE 155/156 jika pelanggan tidak membutuhkannya.
5. Perintah `security-mgmt 1 state enable mode forward` pada sumber tidak menentukan protocol/scope. Tidak dimasukkan ke template eksekusi: verifikasi fungsi dan dampaknya lewat manual firmware sebelum mempertimbangkannya. TR-069 bukan izin membuka web WAN.
6. Jika gagal, inspeksi state/config dan jalur jaringan. Jangan mengulang mutasi, reset ONT, mematikan firewall, atau menghapus WAN existing. Sintaks undo tidak ada di sumber: verifikasi rencana rollback sebelum perubahan, jangan mengarang command `no`.

## Pitfalls

- Sumber memakai VLAN ACS 1011, WAN 2, TR-069 ID 1 dan profile TR069 sebagai contoh, bukan nilai wajib.
- Ada dua baris `wan-ip 1 ping-response ... traceroute-response ...`; baris kedua mematikan traceroute WAN 1, bukan mengatur WAN 2. Jangan menyalinnya sebagai konfigurasi ACS.
- Sumber tidak membuktikan cara pemilihan management WAN oleh TR-069; WAN ID 2 dan TR-069 ID 1 bukan bukti binding otomatis. Verifikasi perilaku firmware.
- URL/IP dan kredensial contoh tidak boleh dipakai sebagai nilai produksi. Password sumber memiliki tanda baca yang tidak boleh dianggap delimiter universal.
- Tidak tersedia command status TR-069 spesifik atau setup server ACS dalam sumber; jangan membuat perintah fiktif.

## Verifikasi

Baca ulang konfigurasi ONU dan `show gpon remote-onu ip-host <ONU_IF>`. Cocokkan WAN manajemen dan alamat DHCP aktual. Di server ACS, operator wajib melihat perangkat dengan serial yang benar, Inform terbaru setelah perubahan, serta sesi autentikasi sukses. Keberadaan config/IP saja tidak membuktikan ACS aktif. Jangan klaim sukses jika akses log ACS tidak tersedia; tandai verifikasi belum lengkap. Uji ulang layanan utama PPPoE atau bridge dan pastikan akses admin tidak melebar. Simpan permanen hanya setelah hasil dan izin `write`.

## Sumber

https://pastebin.com/pAyGYJLQ
https://pastebin.com/raw/pAyGYJLQ
Adaptasi dengan placeholder dan pengaman; lisensi sumber belum diverifikasi. Belum diuji pada perangkat OLT.
