---
name: zte-olt-onu-trunking
description: Konfigurasi trunk multi-VLAN pada port ONT ZTE.
version: 0.1.0
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [zte, olt, onu, trunk, vlan]
    related_skills: [zte-olt-onu-provisioning, zte-olt-vlan-provisioning]
---
# Trunk dan Multiple Trunking ONT

## Persetujuan pengguna untuk eksekusi berisiko

Wajib minta dan tunggu persetujuan eksplisit pengguna sebelum setiap eksekusi berisiko. Permintaan diagnosis, aktivasi umum, pembuatan skill, atau persetujuan sebelumnya bukan izin untuk tindakan baru.

Sebelum meminta izin, tampilkan target pelanggan/SN/interface/slot, perintah atau kelompok perubahan yang tepat (rahasia disamarkan), dampak layanan/keamanan, potensi kehilangan konfigurasi, dan rencana pemulihan. Eksekusi hanya tindakan dalam lingkup yang disetujui. Pengguna boleh menyetujui satu kelompok perintah yang sudah dijelaskan; perubahan target, perintah, dampak atau langkah pemulihan memerlukan persetujuan baru. Diam atau jawaban ambigu bukan persetujuan.

Termasuk berisiko: registrasi/penghapusan/ganti SN ONU; perubahan VLAN, WAN, port, profile, bandwidth, ACS, Wi-Fi, routing dan akses management; shutdown/unlock/aktivasi PON; DHCP renew; reboot/factory reset/reset-card/swap; perubahan akun/password/SSH/Telnet/SNMP/waktu; penonaktifan proteksi; pembukaan akses remote; serta `write` atau penyimpanan permanen. Rollback yang mengubah perangkat juga harus tercakup izin atau dimintakan izin baru.

Pembacaan status biasa pada target yang sudah diotorisasi dapat dilakukan tanpa izin mutasi tambahan. Jika tingkat risiko tidak jelas, berhenti dan tanyakan. Jangan melanjutkan mutasi otomatis setelah error, timeout atau putus koneksi: periksa kondisi secara baca-saja, lalu minta persetujuan baru bila tindakan lanjutan diperlukan. Dalam proses tanpa pengguna hadir, jangan lakukan tindakan berisiko tanpa persetujuan spesifik yang sudah tercatat.

## Kapan Digunakan
Meneruskan beberapa VLAN tagged dengan satu native/untagged VLAN pada port ONT. Dukungan bergantung model dan firmware.

## Klarifikasi wajib sebelum konfigurasi

Jika permintaan hanya menyebut bridge, tanyakan access atau trunk dahulu. Tanyakan VLAN yang akan diaktifkan dan port eth tujuan. Untuk trunk, minta tagged VLAN list dan native/untagged VLAN (atau tidak ada) per port. Untuk access, satu VLAN untagged per port; jangan menjalankan template trunk untuk access. Jangan mengasumsikan semua VLAN lewat semua port. Jika jawaban sudah eksplisit, konfirmasi dalam ringkasan, tidak perlu tanya ulang.

Validasi port fisik, VLAN 1–4094, mapping per port, tidak ada overlap native/tagged, dan dukungan tagged-only firmware bila diperlukan. Tunggu data lengkap. Saat aktivasi, tanyakan juga tambahan TR-069/ACS ya/tidak, kemudian minta persetujuan ringkasan sebelum mutasi.

## Prosedur
1. Buat matriks VLAN pelanggan, VLAN jaringan, service-port, GEM/vport, dan port ONT. Nyatakan native VLAN terpisah dari tagged list.
2. Pastikan VLAN tersedia dan ditag pada uplink, DBA profile tersedia, serta ONT sudah terdaftar.
3. Contoh satu T-CONT/GEM untuk beberapa VLAN; pilih ID kosong, jangan menimpa layanan:
```text
configure terminal
interface <ONU_IF>
tcont <TCONT_ID> name TRUNKING profile <DBA_PROFILE>
gemport <GEM_ID> name TRUNKING tcont <TCONT_ID>
service-port <SERVICE_PORT_ID> vport <VPORT_ID> user-vlan <CUSTOMER_VLAN> vlan <NETWORK_VLAN>
exit
pon-onu-mng <ONU_IF>
service <SERVICE_NAME> gemport <GEM_ID> vlan <CUSTOMER_VLAN>
vlan port <ETH_IF> mode hybrid def-vlan <NATIVE_VLAN>
vlan port <ETH_IF> vlan <TAGGED_VLAN_LIST>
exit
end
```
Ulangi service-port (ID unik) dan service untuk setiap VLAN, dengan mode CLI yang benar. Mapping vport/GEM harus sesuai firmware, bukan selalu diasumsikan sama.
4. `dhcp-ip ethuni <ETH_IF> from-internet` hanya jika desain memerlukannya. PPPoE routing-mode dapat hidup bersama trunk lewat host terpisah sesuai sumber, tetapi kredensial dan WAN tidak diperlukan untuk trunk murni.

## Pitfalls
Sumber 11 menyediakan service PPPoE VLAN 2542 tetapi tidak memasukkannya ke daftar tagged eth_0/1 karena dipakai WAN internal; jangan otomatis menambahkan semua service VLAN ke port pelanggan. Native VLAN harus konsisten dengan perangkat downstream. Web remote dalam contoh bukan syarat trunk.

## Verifikasi
Baca konfigurasi kedua lapisan ONU, cek `show mac gpon onu <ONU_IF>` dan `show gpon remote-onu interface eth <ONU_IF>`. Uji setiap VLAN tagged dan native secara terpisah dari endpoint; catat hasil per VLAN.

## Prasyarat dan pengaman

Target C320; kompatibilitas C300 wajib dikonfirmasi lewat dokumentasi firmware atau bantuan `?`. Perintah berikut adalah template CLI OLT, bukan perintah shell OS. Gunakan sesi perangkat yang telah diotorisasi atau minta operator menjalankannya; tidak ada koneksi otomatis dalam paket ini.

Validasi identitas OLT, port, SN, ONU ID, VLAN, nama profile, dan seluruh placeholder sebelum penggunaan. VLAN 1–4094; ID dan port harus tersedia serta sesuai kapasitas perangkat. Tolak input berisi newline atau pemisah perintah. Jangan menyalin alamat, serial, password, atau angka contoh sebagai konfigurasi produksi.

Sebelum perubahan: simpan konfigurasi awal, petakan dampak, tentukan rencana pemulihan, dan minta persetujuan target serta perubahan spesifik. Kerjakan satu target dahulu. Berhenti jika command ditolak; jangan mencoba variasi mutasi secara acak. Jangan menyimpan perubahan permanen sebelum verifikasi layanan dan izin penyimpanan. Password diisi operator melalui jalur aman; jangan dicetak ke laporan atau log.

## Tambahan Tembolok: trunk eksplisit

Alternatif sumber pada mode `pon-onu-mng <ONU_IF>`:
```text
vlan port <ETH_IF> mode trunk
vlan port <ETH_IF> vlan <TAGGED_VLAN_LIST>
```
Gunakan setelah dukungan model/firmware terkonfirmasi dan native/tagged requirements jelas. Ini alternatif mode hybrid, bukan command tambahan untuk semua port. Verifikasi perilaku untagged aktual; jangan mengasumsikan native VLAN implisit.

Artikel mencontohkan ONT sebagai uplink OLT downstream. Ini desain cascade, bukan obat jalur optik buruk: perlu link budget, kapasitas shared PON, loop prevention, VLAN isolation dan fault-domain review. Jangan mengaktifkan cascade, web WAN, atau PPPoE otomatis karena template trunk memuatnya.
