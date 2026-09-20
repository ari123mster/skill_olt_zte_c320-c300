---
name: zte-olt-gpon-profiles
description: Buat profile DBA, VLAN, ONU-type, line dan remote.
version: 0.1.0
platforms: [linux, macos, windows]
---

# Profile GPON ZTE

## Kapan Digunakan
Menyiapkan profile sebelum provisioning ONT. Perubahan profile bersama dapat memengaruhi semua pelanggan pemakainya.

## Prosedur
1. Inventaris profile existing dan pengguna profile lewat konfigurasi aktual. Pilih nama baru untuk menghindari perubahan global tidak sengaja.
2. Definisikan DBA sesuai SLA. Bentuk dari sumber; pilih satu tipe per profile, jangan menjalankan seluruh variasi dengan nama sama:
```text
configure terminal
gpon
profile tcont <PROFILE> type 1 fixed <RATE>
profile tcont <PROFILE> type 2 assured <RATE>
profile tcont <PROFILE> type 3 assured <ASSURED> maximum <MAXIMUM>
profile tcont <PROFILE> type 4 maximum <MAXIMUM>
```
Sumber memakai angka 1024–32768 tanpa definisi unit eksplisit. Pastikan unit dan rentang melalui manual firmware; jangan menganggap byte/s atau Mbps.
3. Dari mode `gpon`, buat profile VLAN:
```text
onu profile vlan <VLAN_PROFILE> tag-mode tag cvlan <CVLAN> pri <PRIORITY>
```
Priority harus 0–7; nilai 7 di sumber bukan default yang harus diikuti.
4. Dari mode konfigurasi global masuk `pon` untuk ONU-type. Kapasitas dan interface harus cocok model aktual:
```text
pon
onu-type <TYPE> gpon description <DESCRIPTION>
onu-type <TYPE> gpon max-tcont <COUNT>
onu-type <TYPE> gpon max-flow-perswitch <COUNT>
onu-type <TYPE> gpon max-iphost <COUNT>
onu-type-if <TYPE> <INTERFACE>
uncfg-onu-display-info model version mac sn pw vendorid
```
Ulangi `onu-type-if` hanya untuk port nyata: eth, pots, wifi. Perintah display-info dapat menampilkan password; jangan aktifkan field `pw` tanpa kebutuhan dan proteksi output.
5. Dari konfigurasi global buat line profile:
```text
onu-profile gpon line <LINE_PROFILE>
tcont <TCONT_ID> name <SERVICE_NAME> profile <DBA_PROFILE>
gemport <GEM_ID> name <SERVICE_NAME> tcont <TCONT_ID>
```
6. Dari konfigurasi global buat remote profile:
```text
onu-profile gpon remote <REMOTE_PROFILE>
service <SERVICE_NAME> gemport <GEM_ID> vlan <VLAN>
vlan port <ETH_IF> mode tag vlan <VLAN>
```
Opsional hanya bila desain perlu dan perangkat mendukung: `interface eth <ETH_IF> mtu <MTU>` dan `dhcp-ip ethuni <ETH_IF> from-internet`. Jangan menyalin MTU 8192 tanpa dukungan end-to-end.

## Pitfalls
Sumber 04 memakai VLAN 2545 pada eth_0/1 yang tidak tercantum pada daftar service. Jangan salin ketidaksesuaian ini. Sumber 06 berjudul with line profile tetapi isinya konfigurasi manual, bukan perintah binding profile. Sintaks binding profile tidak disediakan; jangan mengarangnya.

## Verifikasi
Baca ulang konfigurasi memakai perintah firmware yang sudah dikonfirmasi. Semua T-CONT/GEM/VLAN/port harus punya pemetaan konsisten. Profile dibuat belum berarti diterapkan ke ONT. Lakukan pilot satu ONT sebelum pemakaian massal.

## Prasyarat dan pengaman

Target C320; kompatibilitas C300 wajib dikonfirmasi lewat dokumentasi firmware atau bantuan `?`. Perintah berikut adalah template CLI OLT, bukan perintah shell OS. Gunakan sesi perangkat yang telah diotorisasi atau minta operator menjalankannya; tidak ada koneksi otomatis dalam paket ini.

Validasi identitas OLT, port, SN, ONU ID, VLAN, nama profile, dan seluruh placeholder sebelum penggunaan. VLAN 1–4094; ID dan port harus tersedia serta sesuai kapasitas perangkat. Tolak input berisi newline atau pemisah perintah. Jangan menyalin alamat, serial, password, atau angka contoh sebagai konfigurasi produksi.

Sebelum perubahan: simpan konfigurasi awal, petakan dampak, tentukan rencana pemulihan, dan minta persetujuan target serta perubahan spesifik. Kerjakan satu target dahulu. Berhenti jika command ditolak; jangan mencoba variasi mutasi secara acak. Jangan menyimpan perubahan permanen sebelum verifikasi layanan dan izin penyimpanan. Password diisi operator melalui jalur aman; jangan dicetak ke laporan atau log.

## Sumber

Randy Filan (randifilan), zte-c320; adaptasi prosedural. Lisensi sumber belum diverifikasi; tidak diberi lisensi baru.
https://github.com/randifilan/zte-c320/tree/bee34b4794055c7c67c32216c471cbb675342ca7
