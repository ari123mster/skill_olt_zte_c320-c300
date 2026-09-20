---
name: zte-olt-onu-provisioning
description: Daftarkan ONU dan layanan PPPoE atau CCTV ZTE.
version: 0.1.0
platforms: [linux, macos, windows]
---

# Registrasi ONU dan Layanan PPPoE/CCTV

## Kapan Digunakan
Registrasi ONU baru melalui SN, PPPoE routing-mode, atau layanan tambahan CCTV/bridge. Bukan perubahan serial ONU existing.

## Wajib klarifikasi sebelum aktivasi

Permintaan seperti "aktivasi pelanggan A" belum memberi izin memilih mode layanan. Sebelum menyusun konfigurasi final atau menjalankan mutasi, tanyakan: "Pelanggan A mau diaktifkan sebagai PPPoE di ONT atau bridge ke router pelanggan?" Jangan memilih PPPoE otomatis, menebak dari pelanggan lain, atau menganggap bridge hanya untuk CCTV. Jika pengguna sudah menyebut mode dengan jelas pada permintaan saat ini, konfirmasi dalam ringkasan tanpa menanyakan ulang.

1. Tentukan mode terlebih dahulu: PPPoE di ONT atau bridge. Jika kebutuhan campuran, klarifikasi mode per layanan dan port.
2. Lengkapi data yang belum tersedia: identitas pelanggan, OLT/PON, SN, model/ONU-type, ONU ID kosong, VLAN pelanggan/jaringan, serta paket/profile bandwidth. Data hasil inspeksi baca-saja boleh dipakai setelah dicocokkan dengan target.
3. Untuk PPPoE di ONT, konfirmasi akun PPPoE dan VLAN profile. Jangan meminta password ditempel di chat; operator memasukkannya melalui jalur aman. Untuk bridge, konfirmasi port LAN, VLAN native/untagged atau tagged list, serta perangkat yang melakukan PPPoE/DHCP. PPPoE di router pelanggan tetap berarti ONT mode bridge.
4. Tampilkan ringkasan pelanggan, SN/interface, mode, profile bandwidth, VLAN mapping, port, dampak, dan rencana pemulihan. Jangan tampilkan password. Minta persetujuan eksplisit atas ringkasan tersebut.
5. Jika mode atau data wajib belum lengkap, berhenti dan tunggu jawaban. Tidak ada registrasi, konfigurasi WAN, perubahan port, atau penyimpanan konfigurasi sebelum persetujuan.

## Wajib tanya tambahan TR-069/ACS

Setelah PPPoE/bridge dipilih, tanyakan: "Mau ditambah TR-069/ACS atau tidak?" Jangan menganggap tidak menjawab berarti tidak, dan jangan aktifkan ACS otomatis. Jika pilihan sudah eksplisit, cukup masukkan ke ringkasan.

- Ya: gunakan `zte-olt-onu-tr069-acs`; lengkapi URL ACS, jalur/VLAN, DHCP/routing, profile, ID kosong, dukungan firmware, dan autentikasi melalui jalur aman. Jangan meminta password di chat.
- Tidak: lewati seluruh penambahan ACS. Jangan hapus ACS existing tanpa instruksi terpisah.
- Belum dijawab: tunggu sebelum konfigurasi final dan mutasi aktivasi.

Ringkasan persetujuan wajib mencantumkan mode utama dan TR-069 ya/tidak, ditambah detail ACS bila ya. Jangan menjalankan template PPPoE/CCTV sebelum pilihan tambahan ini selesai.

## Pemilihan alur

- PPPoE di ONT: gunakan template PPPoE pada prosedur berikut hanya setelah klarifikasi dan persetujuan.
- Bridge: jangan menjalankan baris `wan-ip ... mode pppoe` atau meminta kredensial PPPoE untuk ONT. Susun pemetaan T-CONT/GEM/service-port/service dan port Ethernet sesuai VLAN yang disetujui. Untuk trunk/multi-VLAN gunakan prosedur `zte-olt-onu-trunking`; jangan menyalin ID/profile CCTV sebagai default Internet bridge. Jika sintaks bridge model tersebut belum terkonfirmasi, berhenti untuk verifikasi firmware, bukan beralih ke PPPoE.
- Verifikasi bridge dari trafik/MAC/VLAN dan koneksi perangkat downstream. IP-host ONT atau sesi PPPoE pada ONT bukan syarat sukses bridge.

## Prosedur
1. Cari perangkat: `show gpon onu uncfg`. Cocokkan SN fisik, port PON, model dan tiket. ONU ID pada discovery bukan otomatis ID final; cek ID yang kosong melalui state dan konfigurasi PON.
2. Pastikan ONU-type, DBA, VLAN profile, VLAN uplink, serta akun AAA/PPPoE sudah tersedia. Jangan membuat akun contoh sumber.
3. Daftarkan target yang disetujui:
```text
configure terminal
interface <OLT_IF>
onu <ONU_ID> type <ONU_TYPE> sn <SERIAL_NUMBER>
exit
interface <ONU_IF>
tcont 1 name PPPoE profile <DBA_INTERNET>
gemport 1 name INTERNET tcont 1
service-port 1 vport 1 user-vlan <CUSTOMER_VLAN> vlan <NETWORK_VLAN>
exit
pon-onu-mng <ONU_IF>
service PPPoE gemport 1 vlan <CUSTOMER_VLAN>
wan-ip 1 mode pppoe username <PPPOE_USER> password <PPPOE_PASSWORD> vlan-profile <VLAN_PROFILE> host 1
exit
end
```
WAN VLAN profile harus sesuai VLAN pada sisi ONU. Untuk mode tanpa translasi, customer/network VLAN sama. Angka T-CONT/GEM/service-port 1 hanya untuk ONU baru yang slot ID-nya kosong.
4. Layanan CCTV opsional, gunakan ID bebas dan pemetaan yang telah disetujui:
```text
configure terminal
interface <ONU_IF>
tcont 2 name CCTV profile <DBA_CCTV>
gemport 2 name CCTV tcont 2
service-port 2 vport 2 user-vlan <CCTV_CUSTOMER_VLAN> vlan <CCTV_NETWORK_VLAN>
exit
pon-onu-mng <ONU_IF>
service CCTV gemport 2 vlan <CCTV_CUSTOMER_VLAN>
vlan port <ETH_IF> mode hybrid def-vlan <CCTV_CUSTOMER_VLAN>
exit
end
```
5. Sumber mengaktifkan ping/traceroute WAN dan web remote bersama PPPoE. Keduanya tidak wajib; jangan aktifkan web remote sebagai efek samping registrasi.

## Pitfalls
Dokumen 06 mencampur CCTV 2546 dan def-vlan 1546 tanpa mapping konsisten. Template ini memaksa pemilihan customer/network VLAN eksplisit. Jangan menerapkan profile line hanya karena judul sumber mengatakannya; contoh isinya manual. Akun PPPoE/AAA dikelola operator melalui prosedur terpisah; jangan membocorkan kredensial dalam output.

## Verifikasi
`show gpon onu state <OLT_IF> <ONU_ID>`, `show gpon onu detail-info <ONU_IF>`, `show run interface <ONU_IF>`, `show onu running config <ONU_IF>`, `show gpon remote-onu ip-host <ONU_IF>`, `show mac gpon onu <ONU_IF>`. Operator mengecek sesi PPPoE di router/AAA dan layanan CCTV dari endpoint. Jangan klaim Internet berhasil hanya dari state working.

## Prasyarat dan pengaman

Target C320; kompatibilitas C300 wajib dikonfirmasi lewat dokumentasi firmware atau bantuan `?`. Perintah berikut adalah template CLI OLT, bukan perintah shell OS. Gunakan sesi perangkat yang telah diotorisasi atau minta operator menjalankannya; tidak ada koneksi otomatis dalam paket ini.

Validasi identitas OLT, port, SN, ONU ID, VLAN, nama profile, dan seluruh placeholder sebelum penggunaan. VLAN 1–4094; ID dan port harus tersedia serta sesuai kapasitas perangkat. Tolak input berisi newline atau pemisah perintah. Jangan menyalin alamat, serial, password, atau angka contoh sebagai konfigurasi produksi.

Sebelum perubahan: simpan konfigurasi awal, petakan dampak, tentukan rencana pemulihan, dan minta persetujuan target serta perubahan spesifik. Kerjakan satu target dahulu. Berhenti jika command ditolak; jangan mencoba variasi mutasi secara acak. Jangan menyimpan perubahan permanen sebelum verifikasi layanan dan izin penyimpanan. Password diisi operator melalui jalur aman; jangan dicetak ke laporan atau log.

## Sumber

Randy Filan (randifilan), zte-c320; adaptasi prosedural. Lisensi sumber belum diverifikasi; tidak diberi lisensi baru.
https://github.com/randifilan/zte-c320/tree/bee34b4794055c7c67c32216c471cbb675342ca7
