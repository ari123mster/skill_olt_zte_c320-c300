---
name: zte-olt-onu-trunking
description: Konfigurasi trunk multi-VLAN pada port ONT ZTE.
version: 0.1.0
platforms: [linux, macos, windows]
---

# Trunk dan Multiple Trunking ONT

## Kapan Digunakan
Meneruskan beberapa VLAN tagged dengan satu native/untagged VLAN pada port ONT. Dukungan bergantung model dan firmware.

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

## Sumber

Randy Filan (randifilan), zte-c320; adaptasi prosedural. Lisensi sumber belum diverifikasi; tidak diberi lisensi baru.
https://github.com/randifilan/zte-c320/tree/bee34b4794055c7c67c32216c471cbb675342ca7
