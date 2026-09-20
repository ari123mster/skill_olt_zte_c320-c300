---
name: zte-olt-bootstrap-management
description: Siapkan chassis dan jaringan manajemen OLT ZTE.
version: 0.1.0
platforms: [linux, macos, windows]
---

# Bootstrap dan Manajemen OLT

## Kapan Digunakan
OLT baru atau perubahan akses manajemen. Bukan template untuk menimpa OLT produksi.

## Prosedur
1. Inventaris chassis/card melalui `show card` dan versi melalui `show system-group`. Pastikan console/out-of-band dan jaringan terisolasi tersedia.
2. Sumber menyebut IP awal `136.1.1.100/24` dan Telnet; ini bukan jaminan default semua perangkat. Hindari Telnet pada jaringan tidak tepercaya karena tidak terenkripsi. Utamakan akses aman yang didukung firmware.
3. Hanya untuk hardware C320 yang cocok, sumber memberi contoh berikut. Jangan menerapkan card/slot yang tidak terpasang:
```text
conf t
set-pnp enable
add-rack rackno 1 racktype C320Rack
add-shelf rackno 1 shelfno 1 shelftype C320_SHELF
add-card rackno 1 shelfno 1 slotno 2 GTGH
add-card rackno 1 shelfno 1 slotno 3 PRAM
add-subcard rackno 1 shelfno 1 slotno 4 subcardno 1 UCDC/1
```
4. Alamat out-of-band, gunakan subnet yang sudah disetujui:
```text
conf t
interface mng1
ip address <MGMT_IP> <NETMASK>
exit
end
```
5. Alternatif in-band; jangan mengganti default route produksi tanpa analisis routing:
```text
conf t
vlan <MGMT_VLAN>
exit
interface vlan<MGMT_VLAN>
ip address <MGMT_IP> <NETMASK>
exit
ip route 0.0.0.0 0.0.0.0 <GATEWAY>
end
```
6. Tag management VLAN pada uplink sesuai media dan konfigurasi upstream. Instruksi tagging tersedia pada skill VLAN provisioning.
7. Opsional timeout Telnet di mode konfigurasi: `line telnet idle-timeout 15`. Ini bukan pengamanan transport.
8. Sesudah verifikasi dan izin penyimpanan, jalankan `write` dari mode privileged.

## Pitfalls
Perubahan IP/route dapat memutus sesi sendiri. PNP dan inventaris chassis bukan langkah wajib semua instalasi. C300 tidak memakai template chassis C320 ini.

## Verifikasi
`show card`, `show system-group`, `show vlan <MGMT_VLAN>`. Operator menguji akses dari jaringan manajemen dan jalur pemulihan; catat hasil aktual sebelum `write`.

## Prasyarat dan pengaman

Target C320; kompatibilitas C300 wajib dikonfirmasi lewat dokumentasi firmware atau bantuan `?`. Perintah berikut adalah template CLI OLT, bukan perintah shell OS. Gunakan sesi perangkat yang telah diotorisasi atau minta operator menjalankannya; tidak ada koneksi otomatis dalam paket ini.

Validasi identitas OLT, port, SN, ONU ID, VLAN, nama profile, dan seluruh placeholder sebelum penggunaan. VLAN 1–4094; ID dan port harus tersedia serta sesuai kapasitas perangkat. Tolak input berisi newline atau pemisah perintah. Jangan menyalin alamat, serial, password, atau angka contoh sebagai konfigurasi produksi.

Sebelum perubahan: simpan konfigurasi awal, petakan dampak, tentukan rencana pemulihan, dan minta persetujuan target serta perubahan spesifik. Kerjakan satu target dahulu. Berhenti jika command ditolak; jangan mencoba variasi mutasi secara acak. Jangan menyimpan perubahan permanen sebelum verifikasi layanan dan izin penyimpanan. Password diisi operator melalui jalur aman; jangan dicetak ke laporan atau log.

## Sumber

Randy Filan (randifilan), zte-c320; adaptasi prosedural. Lisensi sumber belum diverifikasi; tidak diberi lisensi baru.
https://github.com/randifilan/zte-c320/tree/bee34b4794055c7c67c32216c471cbb675342ca7
