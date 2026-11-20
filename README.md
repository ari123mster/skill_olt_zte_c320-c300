# Paket skill OLT ZTE C300/C320

20 skill mandiri; dokumen saja, belum diinstal atau diuji pada OLT.

Inventaris koneksi: olt_connections.xlsx, sheet OLT; password diganti Credential_Ref. Rahasia disimpan di KeePassXC olt_credentials.kdbx, dibuat pengguna secara lokal. Panduan Windows/Linux: MIGRASI.md. Tidak ada profil nyata atau koneksi otomatis.

Skill tambahan: zte-olt-connection-inventory — tambah/update host, SSH/Telnet, port, username dan referensi vault dalam Excel; password hanya di KeePassXC.

Skill tambahan untuk review: zte-olt-onu-pon-migration — pemindahan ONU antar-PON pada OLT yang sama, backup, persetujuan cutover, verifikasi dan rollback; belum diuji perangkat.

## Daftar fungsi

1. zte-olt-onu-diagnostics — state individual/PON/global, uncfg, optik, trafik, uptime, histori, MAC, model dan versi.
2. zte-olt-onu-config-audit — audit interface, ONU management, section/filter, VLAN dan service mapping.
3. zte-olt-onu-access-management — pencarian SN, Ethernet, Wi-Fi, IP-host, lock/unlock, DHCP renew.
4. zte-olt-onu-lifecycle — reboot dan factory reset.
5. zte-olt-system-health — uptime, board, CPU, memori, suhu, detail slot.
6. zte-olt-uplink-vlan-operations — diagnosis uplink/VLAN, reset card, switchover.
7. zte-olt-bootstrap-management — chassis C320, out-of-band, in-band, route, persistence.
8. zte-olt-gpon-profiles — DBA/T-CONT, VLAN profile, ONU-type, line dan remote profile.
9. zte-olt-vlan-provisioning — VLAN layanan, tagging uplink dan opsi multicast.
10. zte-olt-onu-provisioning — registrasi SN, PPPoE, CCTV, translasi VLAN.
11. zte-olt-onu-trunking — trunk tagged/native dan multiple trunking.
12. zte-olt-onu-wan-web — akses web WAN terbatas, bukan default provisioning.
13. zte-olt-onu-serial-replacement — penggantian binding serial ONT existing.
14. zte-olt-onu-tr069-acs — tambahan ACS opsional; wajib tanya ya/tidak saat aktivasi.
15. zte-olt-clock-ntp — jam, timezone dan NTP.
16. zte-olt-snmp-management — community dan monitoring SNMP.
17. zte-olt-admin-ssh — akun administrator dan SSH.
18. zte-olt-onu-decommission — penghapusan registrasi ONU.
19. zte-olt-connection-inventory — inventaris koneksi Excel dan referensi vault KeePassXC.
20. zte-olt-onu-pon-migration — pemindahan ONU antar-PON pada OLT yang sama (draft untuk review).

Tambahan Tembolok: https://www.tembolok.id/setting-olt-zte-c320-via-console-terminal-telnet/
Console/PON/management: bootstrap-management; NTP: clock-ntp; SNMP: snmp-management; akun/SSH: admin-ssh; status uplink: uplink-vlan-operations; DBA tipe 5/GEM traffic/show profile: gpon-profiles; discovery/optik PON: onu-diagnostics; binding WAN eth/SSID/hotspot: onu-provisioning; hapus ONU: onu-decommission; trunk eksplisit/cascade: onu-trunking; audit: onu-config-audit. Topik lain digabung dengan skill existing. Klaim kapasitas/speed yang tidak konsisten serta contoh WEP/open Wi-Fi diberi pengaman, bukan default otomatis.

## Referensi silang Idrus Firmansyah

https://idrusfirmansyah.blogspot.com/2018/07/10-basic-command-di-olt-gpon-zte.html
Judul aktual: 12 Text CLI Populer di OLT GPON ZTE. Semua 12 topik telah tersedia:
- Nomor 1 dan 11 (config interface/PON ONU): onu-config-audit.
- Nomor 2–7 (state, optik, trafik, histori, MAC, versi): onu-diagnostics.
- Nomor 8 dan 10 (status Ethernet, lock port): onu-access-management.
- Nomor 9 dan 12 (reboot, factory reset): onu-lifecycle.
Tidak dibuat skill duplikat. Contoh konfigurasi output bukan instruksi provisioning otomatis; ketentuan persetujuan eksekusi berisiko tetap berlaku. Link artikel terkait di sidebar tidak termasuk cakupan pemeriksaan ini.

## Sumber
| Dokumen | Skill tujuan |
|---|---|
| 00. Defaut Config.md | bootstrap-management |
| 01. Basic Config OLT ZTE.md | diagnostics, access-management, lifecycle, system-health, provisioning, uplink-vlan-operations |
| 02. Configure GPON Profile Tcont, VLAN, onu-type.md | gpon-profiles |
| 03. Configure VLAN and Uplink Port.md | vlan-provisioning |
| 04. Configure GPON Profile Line and Profile Remote.md | gpon-profiles |
| 05. Register ONU with PPPoE (without line profile).md | onu-provisioning |
| 06. Register ONU with PPPoE and CCTV VLAN (with line profile).md | onu-provisioning |
| 07. Change ONU SN.md | onu-serial-replacement |
| 08. Allow WAN Web Remote.md | onu-wan-web |
| 09. Show ONU Config.md | onu-config-audit |
| 10. Register ONU with Trunk Port.md | onu-trunking |
| 11. Multiple Trunking.md | onu-trunking |
| README.md | atribusi Randy Filan |

Sumber tambahan TR-069/ACS: https://pastebin.com/pAyGYJLQ
Dipetakan ke zte-olt-onu-tr069-acs dan pertanyaan wajib di onu-provisioning.

## Batas adaptasi

- Materi duplikat digabung, tidak dibuat skill duplikat per sumber.
- Contoh akun/password PPPoE dan IP produksi tidak disalin sebagai nilai operasional. Administrasi MikroTik/AAA diserahkan ke operator, bukan skill OLT tersendiri.
- Ketidaksesuaian VLAN 1546/2546 dan remote-profile VLAN 2545 ditandai; tidak dinormalisasi diam-diam.
- Judul sumber 06 menyebut line profile tetapi contoh manual; tidak ada command binding profile yang dikarang.
- HTTP WAN, Telnet, reset, swap, perubahan uplink, dan factory reset diberi batas keamanan/persetujuan.
- Sintaks dan kapasitas bersifat firmware/model-specific. Template chassis C320 tidak boleh dipakai sebagai chassis C300.
- Lisensi sumber belum diverifikasi. Paket tidak menyatakan lisensi ulang atas materi sumber.

## Notasi dan penggunaan

`<ONU_IF>` = `gpon-onu_1/2/5:5`; `<OLT_IF>` = `gpon-olt_1/2/5`; `<ONU_ID>` = `5`.
Triplet interface mengikuti penomoran rack/shelf, slot, port pada CLI perangkat; bukan tiga nilai rack/shelf/slot board. Verifikasi layout model aktual.
`<ETH_IF>` contoh `eth_0/1`; `<UPLINK_IF>` contoh `gei_1/4/3`; `<XGEI_IF>` contoh `xgei_1/21/1`.

Setiap SKILL.md dapat dibaca mandiri. Semua blok perintah merupakan CLI perangkat, bukan shell OS. Ganti placeholder hanya setelah memvalidasi target. `!` dan prompt hostname dari output bukan perintah navigasi. Jangan menyalin semua alternatif sebagai satu batch.

Jalankan validator dokumen dari terminal:
```text
python validate_skills.py
```
Jalankan dari folder paket; path absolut tidak diperlukan.
Validasi dokumen tidak membuktikan kompatibilitas firmware atau keberhasilan pada OLT nyata.

