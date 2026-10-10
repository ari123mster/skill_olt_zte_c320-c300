# Katalog ONU-type offline

Transkripsi lengkap file PON Config ONU-TYPE dari repositori denniseptian/ZTE-C300. Tidak perlu membuka web untuk membaca contoh ini. Angka adalah konfigurasi contoh sumber, bukan spesifikasi hardware terverifikasi.

## Pengaman dan keterbatasan
- Pengguna memilih ONU-type dan profile; ALL/1G bukan default wajib. ONU-type berbeda dari DBA/rate profile; max-tcont bukan bandwidth.
- Periksa tipe existing, firmware OLT, revisi hardware ONT, kemampuan OMCI dan port nyata. Pilih satu tipe beserta onu-type-if miliknya; jangan paste seluruh katalog.
- Setelah persetujuan, konteksnya konfigurasi global lalu pon, sesuai firmware. Sumber tidak menyertakan wrapper mode CLI. Jangan mengarang sintaks yang tidak didukung.
- Nama mirip bukan tipe identik: ZTE-F609 dan ZTEG-F609 memiliki parameter berbeda. OPEN_* bukan jaminan universal.
- Parameter yang tidak tercantum tidak boleh diasumsikan nol atau disalin dari model lain; misalnya max-tcont ZTEG-F670 tidak tercantum.
- Definisi interface tidak lengkap untuk semua tipe: OPEN_FIBERHOME, OPEN_HUAWEI, OPEN_NOKIA, ZTEG-9806H dan ZTEG-MSAG tidak memiliki onu-type-if sama sekali; ZTEG-F625 memakai rf_0/1 untuk CATV; ZTEG-F820 dideskripsikan 24ETH,32POTS tetapi file hanya mencantumkan eth_0/1–4. Jangan menganggap katalog siap pakai untuk model tersebut tanpa melengkapi dari bukti perangkat/vendor.
- service-mgmt-via-non-omci wifi enable hanya dipakai jika diperlukan dan didukung, bukan otomatis.
- Perubahan tipe bersama dapat berdampak semua ONU pemakainya. Backup, pemetaan dampak, persetujuan command/rollback, read-back dan pilot satu ONU wajib. write perlu izin persistensi. Belum diuji perangkat.

## Daftar nama

HUAWEI-HG8245A, HUAWEI-HG8245H, HUAWEI-HG8245U, OPEN_FIBERHOME, OPEN_HUAWEI, OPEN_NOKIA, OPEN_ZTE, ZTE-F609, ZTE-F660, ZTEG-9806H, ZTEG-F600, ZTEG-F609, ZTEG-F620, ZTEG-F625, ZTEG-F627, ZTEG-F660, ZTEG-F670, ZTEG-F820, ZTEG-MSAG, ZXA10-F660.

## Command sumber lengkap

```text
onu-type HUAWEI-HG8245A gpon description 4ETH,2POTS,WIFI
  onu-type HUAWEI-HG8245A gpon max-tcont 40
  onu-type HUAWEI-HG8245A gpon max-switch-perslot 32
  onu-type HUAWEI-HG8245A gpon max-flow-perswitch 200
  onu-type HUAWEI-HG8245A gpon max-iphost 5
  onu-type HUAWEI-HG8245H gpon description 4ETH,2POTS,WIFI
  onu-type HUAWEI-HG8245H gpon max-tcont 40
  onu-type HUAWEI-HG8245H gpon max-switch-perslot 32
  onu-type HUAWEI-HG8245H gpon max-flow-perswitch 200
  onu-type HUAWEI-HG8245H gpon max-iphost 5
  onu-type HUAWEI-HG8245U gpon description 4ETH,2POTS,WIFI
  onu-type HUAWEI-HG8245U gpon max-tcont 40
  onu-type HUAWEI-HG8245U gpon max-switch-perslot 32
  onu-type HUAWEI-HG8245U gpon max-flow-perswitch 200
  onu-type HUAWEI-HG8245U gpon max-iphost 5
  onu-type OPEN_FIBERHOME gpon
  onu-type OPEN_FIBERHOME gpon max-tcont 40
  onu-type OPEN_FIBERHOME gpon max-switch-perslot 32
  onu-type OPEN_FIBERHOME gpon max-flow-perswitch 200
  onu-type OPEN_FIBERHOME gpon max-iphost 5
  onu-type OPEN_HUAWEI gpon
  onu-type OPEN_HUAWEI gpon max-tcont 40
  onu-type OPEN_HUAWEI gpon max-switch-perslot 32
  onu-type OPEN_HUAWEI gpon max-flow-perswitch 200
  onu-type OPEN_HUAWEI gpon max-iphost 5
  onu-type OPEN_NOKIA gpon
  onu-type OPEN_NOKIA gpon max-tcont 40
  onu-type OPEN_NOKIA gpon max-switch-perslot 32
  onu-type OPEN_NOKIA gpon max-flow-perswitch 200
  onu-type OPEN_NOKIA gpon max-iphost 5
  onu-type OPEN_ZTE gpon
  onu-type OPEN_ZTE gpon max-tcont 40
  onu-type OPEN_ZTE gpon max-switch-perslot 32
  onu-type OPEN_ZTE gpon max-flow-perswitch 200
  onu-type OPEN_ZTE gpon max-iphost 5
  onu-type ZTE-F609 gpon description 4ETH,2POTS,WIFI
  onu-type ZTE-F609 gpon max-tcont 7
  onu-type ZTE-F609 gpon max-gemport 32
  onu-type ZTE-F609 gpon max-switch-perslot 8
  onu-type ZTE-F609 gpon max-flow-perswitch 32
  onu-type ZTE-F609 gpon max-iphost 5
  onu-type ZTE-F609 gpon service-mgmt-via-non-omci wifi enable
  onu-type ZTE-F660 gpon description 4ETH,2POTS,WIFI
  onu-type ZTE-F660 gpon max-tcont 7
  onu-type ZTE-F660 gpon max-gemport 32
  onu-type ZTE-F660 gpon max-switch-perslot 8
  onu-type ZTE-F660 gpon max-flow-perswitch 32
  onu-type ZTE-F660 gpon max-iphost 5
  onu-type ZTE-F660 gpon service-mgmt-via-non-omci wifi enable
  onu-type ZTEG-9806H gpon description 1ETH
  onu-type ZTEG-9806H gpon max-tcont 40
  onu-type ZTEG-9806H gpon max-switch-perslot 32
  onu-type ZTEG-9806H gpon max-flow-perswitch 200
  onu-type ZTEG-F600 gpon description 4ETH
  onu-type ZTEG-F600 gpon max-tcont 40
  onu-type ZTEG-F600 gpon max-switch-perslot 32
  onu-type ZTEG-F600 gpon max-flow-perswitch 200
  onu-type ZTEG-F609 gpon description 4eth,2pots,4wifi
  onu-type ZTEG-F609 gpon max-tcont 40
  onu-type ZTEG-F609 gpon max-switch-perslot 32
  onu-type ZTEG-F609 gpon max-flow-perswitch 200
  onu-type ZTEG-F609 gpon max-iphost 5
  onu-type ZTEG-F620 gpon description 4ETH,2POTS
  onu-type ZTEG-F620 gpon max-tcont 40
  onu-type ZTEG-F620 gpon max-switch-perslot 32
  onu-type ZTEG-F620 gpon max-flow-perswitch 200
  onu-type ZTEG-F625 gpon description 4ETH,2POTS,1CATV
  onu-type ZTEG-F625 gpon max-tcont 40
  onu-type ZTEG-F625 gpon max-switch-perslot 32
  onu-type ZTEG-F625 gpon max-flow-perswitch 200
  onu-type ZTEG-F627 gpon description 4ETH,2POTS
  onu-type ZTEG-F627 gpon max-tcont 40
  onu-type ZTEG-F627 gpon max-switch-perslot 32
  onu-type ZTEG-F627 gpon max-flow-perswitch 200
  onu-type ZTEG-F660 gpon description 4ETH,2POTS,4WIFI
  onu-type ZTEG-F660 gpon max-tcont 40
  onu-type ZTEG-F660 gpon max-switch-perslot 32
  onu-type ZTEG-F660 gpon max-flow-perswitch 200
  onu-type ZTEG-F660 gpon max-iphost 5
  onu-type ZTEG-F670 gpon description 4ETH,2POTS,WIFI
  onu-type ZTEG-F670 gpon max-switch-perslot 32
  onu-type ZTEG-F670 gpon max-flow-perswitch 200
  onu-type ZTEG-F670 gpon max-iphost 5
  onu-type ZTEG-F820 gpon description 24ETH,32POTS
  onu-type ZTEG-F820 gpon max-tcont 40
  onu-type ZTEG-F820 gpon max-switch-perslot 32
  onu-type ZTEG-F820 gpon max-flow-perswitch 200
  onu-type ZTEG-F820 gpon max-iphost 3
  onu-type ZTEG-MSAG gpon description 1ETH
  onu-type ZTEG-MSAG gpon max-tcont 40
  onu-type ZTEG-MSAG gpon max-switch-perslot 32
  onu-type ZTEG-MSAG gpon max-flow-perswitch 200
  onu-type ZXA10-F660 gpon description 4ETH,2POTS,WIFI
  onu-type ZXA10-F660 gpon max-tcont 7
  onu-type ZXA10-F660 gpon max-gemport 32
  onu-type ZXA10-F660 gpon max-switch-perslot 8
  onu-type ZXA10-F660 gpon max-flow-perswitch 32
  onu-type ZXA10-F660 gpon max-iphost 5
  onu-type ZXA10-F660 gpon service-mgmt-via-non-omci wifi enable
  onu-type-if HUAWEI-HG8245A eth_0/1
  onu-type-if HUAWEI-HG8245A eth_0/2
  onu-type-if HUAWEI-HG8245A eth_0/3
  onu-type-if HUAWEI-HG8245A eth_0/4
  onu-type-if HUAWEI-HG8245A pots_0/1
  onu-type-if HUAWEI-HG8245A pots_0/2
  onu-type-if HUAWEI-HG8245A wifi_0/1
  onu-type-if HUAWEI-HG8245A wifi_0/2
  onu-type-if HUAWEI-HG8245A wifi_0/3
  onu-type-if HUAWEI-HG8245A wifi_0/4
  onu-type-if HUAWEI-HG8245H eth_0/1
  onu-type-if HUAWEI-HG8245H eth_0/2
  onu-type-if HUAWEI-HG8245H eth_0/3
  onu-type-if HUAWEI-HG8245H eth_0/4
  onu-type-if HUAWEI-HG8245H pots_0/1
  onu-type-if HUAWEI-HG8245H pots_0/2
  onu-type-if HUAWEI-HG8245H wifi_0/1
  onu-type-if HUAWEI-HG8245H wifi_0/2
  onu-type-if HUAWEI-HG8245H wifi_0/3
  onu-type-if HUAWEI-HG8245H wifi_0/4
  onu-type-if HUAWEI-HG8245U eth_0/1
  onu-type-if HUAWEI-HG8245U eth_0/2
  onu-type-if HUAWEI-HG8245U eth_0/3
  onu-type-if HUAWEI-HG8245U eth_0/4
  onu-type-if HUAWEI-HG8245U pots_0/1
  onu-type-if HUAWEI-HG8245U pots_0/2
  onu-type-if HUAWEI-HG8245U wifi_0/1
  onu-type-if HUAWEI-HG8245U wifi_0/2
  onu-type-if HUAWEI-HG8245U wifi_0/3
  onu-type-if HUAWEI-HG8245U wifi_0/4
  onu-type-if OPEN_ZTE eth_0/1
  onu-type-if OPEN_ZTE eth_0/2
  onu-type-if OPEN_ZTE eth_0/3
  onu-type-if OPEN_ZTE eth_0/4
  onu-type-if OPEN_ZTE pots_0/1
  onu-type-if OPEN_ZTE pots_0/2
  onu-type-if ZTE-F609 eth_0/1
  onu-type-if ZTE-F609 eth_0/2
  onu-type-if ZTE-F609 eth_0/3
  onu-type-if ZTE-F609 eth_0/4
  onu-type-if ZTE-F609 pots_0/1
  onu-type-if ZTE-F609 pots_0/2
  onu-type-if ZTE-F609 wifi_0/1
  onu-type-if ZTE-F609 wifi_0/2
  onu-type-if ZTE-F609 wifi_0/3
  onu-type-if ZTE-F609 wifi_0/4
  onu-type-if ZTE-F660 eth_0/1
  onu-type-if ZTE-F660 eth_0/2
  onu-type-if ZTE-F660 eth_0/3
  onu-type-if ZTE-F660 eth_0/4
  onu-type-if ZTE-F660 pots_0/1
  onu-type-if ZTE-F660 pots_0/2
  onu-type-if ZTE-F660 wifi_0/1
  onu-type-if ZTE-F660 wifi_0/2
  onu-type-if ZTE-F660 wifi_0/3
  onu-type-if ZTE-F660 wifi_0/4
  onu-type-if ZTEG-F600 eth_0/1
  onu-type-if ZTEG-F600 eth_0/2
  onu-type-if ZTEG-F600 eth_0/3
  onu-type-if ZTEG-F600 eth_0/4
  onu-type-if ZTEG-F609 eth_0/1
  onu-type-if ZTEG-F609 eth_0/2
  onu-type-if ZTEG-F609 eth_0/3
  onu-type-if ZTEG-F609 eth_0/4
  onu-type-if ZTEG-F609 pots_0/1
  onu-type-if ZTEG-F609 pots_0/2
  onu-type-if ZTEG-F609 wifi_0/1
  onu-type-if ZTEG-F609 wifi_0/2
  onu-type-if ZTEG-F609 wifi_0/3
  onu-type-if ZTEG-F609 wifi_0/4
  onu-type-if ZTEG-F620 eth_0/1
  onu-type-if ZTEG-F620 eth_0/2
  onu-type-if ZTEG-F620 eth_0/3
  onu-type-if ZTEG-F620 eth_0/4
  onu-type-if ZTEG-F620 pots_0/1
  onu-type-if ZTEG-F620 pots_0/2
  onu-type-if ZTEG-F625 eth_0/1
  onu-type-if ZTEG-F625 eth_0/2
  onu-type-if ZTEG-F625 eth_0/3
  onu-type-if ZTEG-F625 eth_0/4
  onu-type-if ZTEG-F625 pots_0/1
  onu-type-if ZTEG-F625 pots_0/2
  onu-type-if ZTEG-F625 rf_0/1
  onu-type-if ZTEG-F627 eth_0/1
  onu-type-if ZTEG-F627 eth_0/2
  onu-type-if ZTEG-F627 eth_0/3
  onu-type-if ZTEG-F627 eth_0/4
  onu-type-if ZTEG-F627 pots_0/1
  onu-type-if ZTEG-F627 pots_0/2
  onu-type-if ZTEG-F660 eth_0/1
  onu-type-if ZTEG-F660 eth_0/2
  onu-type-if ZTEG-F660 eth_0/3
  onu-type-if ZTEG-F660 eth_0/4
  onu-type-if ZTEG-F660 pots_0/1
  onu-type-if ZTEG-F660 pots_0/2
  onu-type-if ZTEG-F660 wifi_0/1
  onu-type-if ZTEG-F660 wifi_0/2
  onu-type-if ZTEG-F660 wifi_0/3
  onu-type-if ZTEG-F660 wifi_0/4
  onu-type-if ZTEG-F670 eth_0/1
  onu-type-if ZTEG-F670 eth_0/2
  onu-type-if ZTEG-F670 eth_0/3
  onu-type-if ZTEG-F670 eth_0/4
  onu-type-if ZTEG-F670 pots_0/1
  onu-type-if ZTEG-F670 pots_0/2
  onu-type-if ZTEG-F670 wifi_0/1
  onu-type-if ZTEG-F670 wifi_0/2
  onu-type-if ZTEG-F670 wifi_0/3
  onu-type-if ZTEG-F670 wifi_0/4
  onu-type-if ZTEG-F670 wifi_0/5
  onu-type-if ZTEG-F670 wifi_0/6
  onu-type-if ZTEG-F670 wifi_0/7
  onu-type-if ZTEG-F670 wifi_0/8
  onu-type-if ZTEG-F820 eth_0/1
  onu-type-if ZTEG-F820 eth_0/2
  onu-type-if ZTEG-F820 eth_0/3
  onu-type-if ZTEG-F820 eth_0/4
```
