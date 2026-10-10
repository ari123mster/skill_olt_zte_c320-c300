---
name: zte-olt-gpon-profiles
description: Buat profile DBA, VLAN, ONU-type, line dan remote.
version: 0.1.0
platforms: [linux, macos, windows]
---

# Profile GPON ZTE

## Persetujuan pengguna untuk eksekusi berisiko

Wajib minta dan tunggu persetujuan eksplisit pengguna sebelum setiap eksekusi berisiko. Permintaan diagnosis, aktivasi umum, pembuatan skill, atau persetujuan sebelumnya bukan izin untuk tindakan baru.

Sebelum meminta izin, tampilkan target pelanggan/SN/interface/slot, perintah atau kelompok perubahan yang tepat (rahasia disamarkan), dampak layanan/keamanan, potensi kehilangan konfigurasi, dan rencana pemulihan. Eksekusi hanya tindakan dalam lingkup yang disetujui. Pengguna boleh menyetujui satu kelompok perintah yang sudah dijelaskan; perubahan target, perintah, dampak atau langkah pemulihan memerlukan persetujuan baru. Diam atau jawaban ambigu bukan persetujuan.

Termasuk berisiko: registrasi/penghapusan/ganti SN ONU; perubahan VLAN, WAN, port, profile, bandwidth, ACS, Wi-Fi, routing dan akses management; shutdown/unlock/aktivasi PON; DHCP renew; reboot/factory reset/reset-card/swap; perubahan akun/password/SSH/Telnet/SNMP/waktu; penonaktifan proteksi; pembukaan akses remote; serta `write` atau penyimpanan permanen. Rollback yang mengubah perangkat juga harus tercakup izin atau dimintakan izin baru.

Pembacaan status biasa pada target yang sudah diotorisasi dapat dilakukan tanpa izin mutasi tambahan. Jika tingkat risiko tidak jelas, berhenti dan tanyakan. Jangan melanjutkan mutasi otomatis setelah error, timeout atau putus koneksi: periksa kondisi secara baca-saja, lalu minta persetujuan baru bila tindakan lanjutan diperlukan. Dalam proses tanpa pengguna hadir, jangan lakukan tindakan berisiko tanpa persetujuan spesifik yang sudah tercatat.

## Kapan Digunakan
Menyiapkan profile sebelum provisioning ONT. Perubahan profile bersama dapat memengaruhi semua pelanggan pemakainya.

## Katalog ONU-type offline

Saat memilih atau membuat ONU-type, baca `references/onu-type-catalog.md` memakai `read_file`. Berisi 20 nama beserta command parameter dan mapping interface yang tersedia dari sumber. Tidak perlu membuka web untuk materi ini. Katalog bukan bukti kompatibilitas semua firmware; perhatikan bagian keterbatasan dan jangan mengarang parameter yang hilang.

ONU-type serta DBA/traffic/VLAN profile mengikuti pilihan pengguna. ALL/1G boleh jika dipilih dan tervalidasi, bukan default wajib. Jangan menjalankan seluruh katalog; pilih hanya tipe dan interface yang disetujui.

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

## Tambahan Tembolok: tipe 5 dan traffic GEM

Baca profile aktual:
```text
show onu-type
show gpon onu profile vlan
show gpon profile tcont
show gpon profile traffic
```
Dari global configuration masuk `gpon`; contoh bentuk tambahan:
```text
profile tcont <DBA_PROFILE> type 5 fixed <FIXED> assured <ASSURED> maximum <MAXIMUM>
profile traffic <TRAFFIC_PROFILE> sir <SIR> pir <PIR>
```
Output sumber menandai FBW/ABW/MBW dan SIR/PIR dalam kbps, CBS/PBS dalam kbytes. Gunakan satuan output firmware, bukan interpretasi nama profile. Untuk menerapkan traffic profile pada GEM, bentuk sumber sebelumnya di interface ONU adalah `gemport <GEM_ID> traffic-limit upstream <UP_PROFILE> downstream <DOWN_PROFILE>`; validasi dukungan dan perubahan rate sebelum penerapan.

Artikel memberi ONU-type gabungan `onu-type <TYPE> gpon max-tcont <N> max-gemport <N> max-switch-perslot <N> max-flow-perswitch <N>` dan `onu-type-if <TYPE> eth_0/1-4` (juga wifi/pots). Range hanya jika model punya port tersebut dan firmware mendukung. Profile bernama ALL tidak membuktikan universal compatibility.

Jangan memakai perhitungan kapasitas artikel sebagai aturan vendor: 1.25 Gbps bukan tepat 1000 Mbps; batas ONU dan budget DBA bergantung card/firmware serta overhead. Bahkan 128 × 8000 kbps = 1,024,000 kbps, bukan ≤1,000,000. `GPONSRV Parameter Exceeds Range` harus dicek terhadap batas profile/resource aktual, bukan otomatis diperbaiki dengan rate tertentu. T-CONT mengalokasikan bandwidth upstream, bukan tunnel simetris. Satu GEM dapat memuat beberapa VLAN seperti contoh trunk sumber lain. Jangan mengubah profile bersama tanpa memetakan pengguna terdampak.


