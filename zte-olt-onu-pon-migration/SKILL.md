---
name: zte-olt-onu-pon-migration
description: Migrasi ONU PPPoE antar-PON; bridge belum didukung.
version: 0.1.0
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [zte, olt, onu, pon, migration]
    related_skills: [zte-olt-onu-decommission, zte-olt-onu-provisioning, zte-olt-onu-diagnostics]
---
# Pindah ONU antar-PON — draft untuk review

Status: prosedur perencanaan berbasis command dasar yang sudah terdokumentasi. Belum diuji di perangkat. Tidak ada command migrasi atomik yang diverifikasi dari sumber; jangan mengarang command move/copy ONU. Penulisan skill tidak memberi izin menjalankan migrasi.

## Persetujuan pengguna untuk eksekusi berisiko

Wajib minta dan tunggu persetujuan eksplisit pengguna sebelum setiap eksekusi berisiko. Permintaan diagnosis, aktivasi umum, pembuatan skill, atau persetujuan sebelumnya bukan izin untuk tindakan baru.

Sebelum meminta izin, tampilkan target pelanggan/SN/interface/slot, perintah atau kelompok perubahan yang tepat (rahasia disamarkan), dampak layanan/keamanan, potensi kehilangan konfigurasi, dan rencana pemulihan. Eksekusi hanya tindakan dalam lingkup yang disetujui. Pengguna boleh menyetujui satu kelompok perintah yang sudah dijelaskan; perubahan target, perintah, dampak atau langkah pemulihan memerlukan persetujuan baru. Diam atau jawaban ambigu bukan persetujuan.

Termasuk berisiko: registrasi/penghapusan/ganti SN ONU; perubahan VLAN, WAN, port, profile, bandwidth, ACS, Wi-Fi, routing dan akses management; shutdown/unlock/aktivasi PON; DHCP renew; reboot/factory reset/reset-card/swap; perubahan akun/password/SSH/Telnet/SNMP/waktu; penonaktifan proteksi; pembukaan akses remote; serta `write` atau penyimpanan permanen. Rollback yang mengubah perangkat juga harus tercakup izin atau dimintakan izin baru.

Pembacaan status biasa pada target yang sudah diotorisasi dapat dilakukan tanpa izin mutasi tambahan. Jika tingkat risiko tidak jelas, berhenti dan tanyakan. Jangan melanjutkan mutasi otomatis setelah error, timeout atau putus koneksi: periksa kondisi secara baca-saja, lalu minta persetujuan baru bila tindakan lanjutan diperlukan. Dalam proses tanpa pengguna hadir, jangan lakukan tindakan berisiko tanpa persetujuan spesifik yang sudah tercatat.

## Batas sementara: hanya pelanggan PPPoE

Skill migrasi ini sementara hanya untuk pelanggan PPPoE dengan terminasi PPPoE di ONT. Migrasi bridge/access/trunk belum didukung dan harus dilewati. PPPoE yang diterminasi di router pelanggan melalui ONT bridge tetap termasuk bridge: jangan dimigrasikan memakai skill ini.

Sebelum perencanaan, konfirmasi mode layanan dari konfigurasi aktual dan pengguna. Jika bridge atau layanan campuran PPPoE + bridge, hentikan rencana migrasi pelanggan tersebut dan jelaskan bahwa dukungan migrasi bridge ditunda. Jangan mengubah bridge menjadi PPPoE agar dapat diproses. Jika mode belum jelas, tanyakan dan jangan melakukan mutasi.

Dalam batch, tandai pelanggan bridge/campuran sebagai SKIP — di luar cakupan sementara, tanpa menghapus binding, mendaftarkan tujuan atau mengubah database pelanggan tersebut. Laporkan daftar yang dilewati dan minta persetujuan daftar akhir PPPoE yang akan diproses. Skill aktivasi bridge terpisah tidak dinonaktifkan; batas ini hanya berlaku untuk migrasi.

Pemeriksaan bridge/trunk hanya untuk mendeteksi pelanggan yang harus dilewati. Jangan melanjutkan melalui skill lain untuk menghindari batas migrasi ini.

## Kapan Digunakan
Memindahkan ONU dengan SN yang sama dari satu port PON ke port PON lain pada OLT ZTE C300/C320 yang sama, sambil mempertahankan layanan PPPoE di ONT yang telah diverifikasi. Bukan penggantian SN, factory reset, atau migrasi lintas OLT. Untuk lintas OLT, berhenti dan minta rencana terpisah karena profile, uplink dan otorisasi dapat berbeda.

Jika pelanggan hanya pindah output splitter/ODP tetapi tetap pada PON yang sama, jangan hapus atau registrasi ulang otomatis. Konfirmasi topologi fisik, verifikasi sinyal dan layanan; perubahan database mungkin tidak diperlukan.

## Klarifikasi wajib

Tanyakan data yang belum tersedia, tidak perlu mengulang data yang sudah eksplisit:
1. Pelanggan dan OLT mana? PON/interface ONU asal dan tujuan?
2. SN tetap atau perangkat juga diganti? Jika SN berubah, pisahkan lingkup penggantian perangkat dari migrasi PON.
3. Apakah kabel sudah dipindah, atau belum? Siapa operator lapangan dan kapan jendela putus layanan disetujui?
4. ONU ID tujuan yang diinginkan atau izin memilih ID kosong? ID asal tidak harus dipakai ulang.
5. Layanan dipertahankan persis atau diubah? Inventaris PPPoE/bridge, access/trunk, mapping VLAN/eth/SSID, bandwidth, ACS, voice/IPTV bila ada.
6. Kriteria sukses, batas waktu gangguan dan kondisi pemicu rollback? Apakah akses jalur lama masih tersedia untuk rollback?

Pertahankan layanan PPPoE di ONT yang sudah terverifikasi; jangan membuat layanan baru atau mengonversi mode dalam migrasi. Jika konfigurasi memuat bridge/trunk atau layanan campuran yang belum didukung, tandai SKIP. ACS existing boleh dipertahankan jika konfigurasi dan dukungannya terverifikasi; penambahan/perubahan ACS merupakan lingkup terpisah dengan persetujuan. Jangan mengganti kredensial atau URL ACS otomatis.

## Pilihan ONU-type dan profile oleh pengguna

ONU-type dan profile tidak dikunci ke `ALL` atau `1G`. Sebelum menyusun rencana migrasi, tanyakan jika belum jelas:
- "ONU-type tujuan mau mempertahankan tipe asal atau menggunakan tipe lain?"
- "Profile T-CONT/bandwidth mau mempertahankan profile asal atau diganti? Nama profile yang dipilih apa?"
- Jika layanan memakai GEM traffic profile, VLAN profile atau line/remote profile, konfirmasi masing-masing yang dipertahankan atau diganti.

`ALL` dan `1G` boleh digunakan jika dipilih eksplisit pengguna, tersedia pada OLT tujuan, sesuai kemampuan ONT, dan lolos pemeriksaan kapasitas/SLA. Jangan menolak hanya karena namanya ALL/1G; jangan pula menganggap nama tersebut membuktikan kompatibilitas atau rate aktual. Periksa isi profile dan ONU-type aktual, lalu tampilkan pilihan dalam ringkasan persetujuan.

Jika pengguna memilih mempertahankan konfigurasi, gunakan nilai asal yang sudah dibaca dan terverifikasi tanpa bertanya ulang setiap parameter. Jika profile pilihan belum tersedia atau tidak kompatibel, berhenti dan jelaskan; jangan membuat profile atau menggantinya diam-diam. Pembuatan/perubahan profile bersama memerlukan rencana dampak dan persetujuan terpisah. Sintaks penerapan line/remote profile tetap harus diverifikasi, bukan dikarang.

## Prasyarat dan pengaman

Konfirmasi OLT/model/firmware, identitas pelanggan dan SN melalui sumber berizin. Template adalah CLI OLT, bukan shell OS. Validasi interface, ID, VLAN dan SN; tolak newline/pemisah command. Jangan menebak batas ONU/kapasitas dari model saja.

## Pra-pemeriksaan baca-saja

```text
show card
show gpon onu by sn <SN>
show gpon onu detail-info <OLD_ONU_IF>
show run interface <OLD_OLT_IF>
show run interface <OLD_ONU_IF>
show onu running config <OLD_ONU_IF>
show gpon onu state <NEW_OLT_IF>
show run interface <NEW_OLT_IF>
show gpon onu uncfg <NEW_OLT_IF>
```

- Cocokkan identitas asal dan pastikan ID tujuan benar-benar kosong dari konfigurasi, bukan hanya tidak terlihat online.
- Pastikan card/PON tujuan siap, ONU-type didukung, batas ONU/T-CONT/GEM dan budget DBA memadai menurut firmware. Membaca state saja tidak membuktikan kapasitas cukup.
- Periksa VLAN/profile layanan dan jalur uplink tujuan. Catat translasi VLAN, GEM/vport/service-port, profile rate, WAN, ACS, LAN/Wi-Fi dan layanan lain dari konfigurasi aktual.
- Ambil baseline optik/MAC/IP-host sesuai layanan. Jika ONU sudah dipindah/offline, tandai data baseline yang tidak tersedia; jangan mengarangnya.
- Simpan backup konfigurasi interface dan ONU management lengkap dalam penyimpanan terlindungi. Password yang disamarkan di output tidak cukup untuk pemulihan; pastikan operator punya sumber kredensial aman sebelum penghapusan.
- Output configuration hanya bukti, bukan script siap paste: hapus prompt/output, sesuaikan mode CLI dan target secara terarah. Jangan melakukan replace angka global yang mengubah VLAN atau ID layanan tanpa sengaja.

## Referensi alur aplikasi pengguna

Referensi yang dibaca: `resources/views/v/olt/migrate.blade.php` dari aplikasi olt-mikrotik milik pengguna. File Blade ini menunjukkan antarmuka/form dan JavaScript, bukan implementasi command migrasi backend. Jangan menyimpulkan urutan delete/register, transaksi database, rollback atau keberhasilan perangkat hanya dari halaman ini. Route `saveMigrate`, endpoint `cekPort`, `getCustomerMigrate`, helper Telnet/parser dan tahap `outMigrateSave` telah diperiksa secara statis; hasilnya ada di references/application-flow.md. Tidak ada endpoint dijalankan.

Alur yang diadopsi:
1. Pilih port sumber, identitas OLT tujuan dan port tujuan secara eksplisit.
2. Ambil daftar ONU sumber beserta SN dan metadata pelanggan; ambil daftar ONU tujuan yang telah terdaftar.
3. Pilih hanya ONU yang diminta, lalu susun daftar review: OLT/PON/ID asal, SN, ID tujuan, Customer ID, nama/deskripsi pelanggan, mapping VLAN dan status ketersediaan kredensial. Password tidak ditampilkan atau disalin ke laporan.
4. Cocokkan setiap baris terhadap konfigurasi aktual dan minta persetujuan sebelum cutover.

Batas penting dari referensi:
- UI menyediakan pilihan OLT tujuan, termasuk kemungkinan OLT berbeda. Itu bukan bukti bahwa skill ini sudah aman untuk lintas OLT. Cakupan eksekusi tetap OLT yang sama; lintas OLT memerlukan rencana terpisah dan verifikasi backend/firmware.
- Input VLAN mencontohkan `3105/3106`; backend `saveMigrate` ternyata mewajibkan satu integer VLAN 1–4094. Contoh slash di UI tidak sesuai validasi backend. Jangan mengirim slash atau menganggap aplikasi mendukung multi-VLAN lewat field tersebut.
- Generator ID UI mencari 1 sampai 1000. Jangan memakai batas 1000 sebagai kapasitas valid OLT. Pakai rentang firmware/card aktual dan periksa ulang ID sebelum registrasi karena snapshot dapat kedaluwarsa.
- Saat source/destination/OLT berubah, buang snapshot, pilihan ONU dan usulan ID yang lama, lalu baca ulang. Array ID tujuan di view ditambahkan pada pencarian; jangan menganggap cache tersebut daftar terkini yang otoritatif.
- Tampilan menggunakan fallback `Unknown`; nilai tersebut bukan identitas yang valid. Data identitas kritis yang hilang harus diklarifikasi, tidak boleh dimigrasikan berdasarkan tebakan.
- Checkbox ALL dan penghapusan baris UI bukan persetujuan massal. Daftar final perlu deduplikasi SN, pemeriksaan ID tujuan unik, jumlah baris yang pasti dan konfirmasi daftar pelanggan. Default satu ONU pilot. Batch hanya atas izin eksplisit; jalankan berurutan dengan hasil per ONU dan berhenti pada kegagalan, bukan menghapus semua sumber dahulu.
- Password PPPoE ditampilkan sebagai teks dan disimpan di atribut/input pada view. Pola ini tidak diadopsi oleh skill: gunakan referensi rahasia/jalur aman; jangan membaca DOM atau dump response berisi password ke konteks model.
- Progress bar adalah animasi CSS, bukan bukti kemajuan eksekusi. Submit/HTTP sukses juga bukan bukti layanan pulih. Verifikasi harus berasal dari state perangkat dan uji layanan.

File aplikasi sumber hanya dibaca sebagai referensi; tidak diubah dan tidak dijalankan. Untuk kelak mengikuti aplikasi persis, periksa controller/service route terkait secara terarah terlebih dahulu tanpa mengeksekusi endpoint mutasi.

## Rencana dan titik persetujuan

Tampilkan ringkasan:
```text
Pelanggan / OLT / SN: ...
Asal: <OLD_OLT_IF>, <OLD_ONU_ID>, <OLD_ONU_IF>
Tujuan: <NEW_OLT_IF>, <NEW_ONU_ID>, <NEW_ONU_IF>
Model / firmware / ONU-type: ...
Layanan dipertahankan / perubahan eksplisit: ...
VLAN, GEM, port LAN/SSID, bandwidth, ACS: ...
Status backup dan kredensial pemulihan: ...
Urutan fisik dan CLI, perkiraan/batas gangguan: ...
Perintah penghapusan, registrasi, reprovisioning: ...
Kriteria rollback, perintah dan operator lapangan: ...
Izin write: terpisah / termasuk persetujuan eksplisit
```

Jangan menghapus registrasi lama sebelum rencana lengkap dan disetujui. Jangan menganggap SN yang sama dapat didaftarkan bersamaan di dua PON: aturan duplikasi bergantung firmware. Jika tidak bisa mempertahankan kedua binding, gunakan cutover delete/re-register hanya setelah backup dan rollback siap serta downtime disetujui. Tidak menjanjikan zero downtime.

## Pelajaran backend dan rekonsiliasi data

Baca `references/application-flow.md` sebelum memakai aplikasi sebagai referensi. Implementasi `saveMigrate` mendaftarkan tujuan dan membangun ulang satu layanan PPPoE; tidak menghapus sumber, tidak menyalin seluruh konfigurasi, tidak memverifikasi layanan dan tidak menjalankan `write`. Jangan menganggap proses aplikasi setara migrasi utuh.

Jangan mewarisi default `type ALL`, profile `1G`, VLAN profile `V<VLAN>`, ping/traceroute aktif atau pembukaan web/Telnet. Cocokkan model, profile aktual dan layanan baseline. Bridge/trunk dan layanan campuran harus SKIP. ACS atau multiple WAN yang tidak dapat dipulihkan lengkap harus menjadi blocker, bukan direduksi menjadi PPPoE tunggal. Periksa respons setiap command dan read-back, bukan satu string Successful dari registrasi saja.

Jika aplikasi/database pelanggan terlibat, pisahkan status: binding tujuan dibuat, layanan terverifikasi, konfigurasi OLT tersimpan, database pelanggan diperbarui, binding asal dibersihkan. Masing-masing memerlukan bukti; satu status tidak menyiratkan yang lain. Jangan menghapus sumber hanya karena UI menyatakan sukses. Urutan pembersihan sumber mengikuti rencana cutover dan batas duplikasi SN firmware, bukan asumsi backend otomatis membersihkannya.

Setelah layanan tujuan terverifikasi, update referensi OLT/port pelanggan hanya dengan izin. Cocokkan identitas record unik dan lokasi lama; Customer ID/username PPPoE tidak otomatis unik global. Tolak hidden-field tujuan yang berbeda dari rencana. Periksa jumlah record yang benar-benar berubah, simpan metadata sebelum/sesudah tanpa rahasia, dan verifikasi read-back. Jika update database gagal, jangan ulang registrasi atau hapus ONU; laporkan ketidaksinkronan dan lakukan rekonsiliasi berizin. Rollback juga harus memulihkan referensi database bila sudah berubah.

Untuk batch, simpan checklist per ONU: belum dimulai, registrasi tujuan, konfigurasi, verifikasi, persistensi, rekonsiliasi DB, gagal/rollback. Pada error, jangan ulang seluruh batch atau menganggap semua belum berubah. Pastikan jumlah dan pasangan field setiap pelanggan lengkap sebelum mutasi.

## Cutover terkontrol

1. Pastikan persetujuan masih cocok target dan kondisi terbaru. Koordinasikan perpindahan kabel sesuai urutan yang disetujui, jangan memerintahkan operator memindah fiber diam-diam. Jangan melihat langsung ke konektor optik aktif.
2. Jika rencana membutuhkan penghapusan binding asal, berikut bentuk dasar yang telah didokumentasikan; ini titik disruptif:
```text
configure terminal
interface <OLD_OLT_IF>
no onu <OLD_ONU_ID>
exit
end
```
3. Periksa output aktual dan kondisi binding. Setelah fiber berada pada jalur tujuan sesuai koordinasi, identifikasi SN melalui discovery tujuan. Jangan mendaftarkan SN lain untuk mengatasi target tidak muncul. Hentikan jika SN/port tidak cocok.
4. Registrasi tujuan dengan ID kosong dan ONU-type yang sudah diverifikasi:
```text
configure terminal
interface <NEW_OLT_IF>
onu <NEW_ONU_ID> type <ONU_TYPE> sn <SN>
exit
end
```
5. Terapkan konfigurasi layanan yang telah direview ke `<NEW_ONU_IF>` menggunakan mode interface dan pon-onu-mng yang tepat. Skill ini tidak memberi template layanan generik karena konfigurasi pelanggan harus dipertahankan. Bila ada perintah profile/OMCI yang belum terverifikasi, berhenti sebelum cutover, bukan improvisasi saat layanan putus.
6. Jangan reset factory, reboot, shutdown seluruh PON, mengubah profile bersama atau menghapus VLAN untuk memaksa migrasi. Jika error/timeout, periksa state baca-saja sebelum tindakan berikutnya; perubahan rencana memerlukan izin baru.

## Verifikasi

```text
show gpon onu by sn <SN>
show gpon onu state <NEW_OLT_IF> <NEW_ONU_ID>
show gpon onu detail-info <NEW_ONU_IF>
show run interface <NEW_ONU_IF>
show onu running config <NEW_ONU_IF>
show pon power attenuation <NEW_ONU_IF>
show mac gpon onu <NEW_ONU_IF>
```

Serial/interface tujuan cocok, binding asal tidak tersisa jika sudah dihapus, konfigurasi sesuai baseline yang disetujui, dan tidak ada konflik ID. Periksa Config state dan alarm. Optik dinilai terhadap budget/spec operator, bukan threshold universal.

Untuk pelanggan PPPoE yang lolos cakupan, uji sesi PPPoE dan trafik pelanggan, binding port Internet, serta ACS Inform terbaru bila ACS dipertahankan. Pelanggan bridge/campuran harus tetap SKIP dan tidak mengalami perubahan binding atau data. Jika baru ditemukan layanan bridge/voice/IPTV tak terdukung saat pelaksanaan, berhenti dan evaluasi pemulihan berizin; jangan mengklaim semua layanan telah dipindahkan. State working atau MAC terpelajari belum cukup. Konfirmasi pelanggan lain pada PON asal/tujuan tidak terdampak. Jika akses pengujian tidak tersedia, nyatakan belum terverifikasi, jangan melaporkan sukses penuh.

`write` hanya setelah verifikasi dan persetujuan persistensi. Laporkan langkah aktual, hasil, kekurangan verifikasi, dan apakah konfigurasi sudah tersimpan; jangan menyatakan sudah tersimpan jika belum dilakukan.

## Rollback

Rollback bukan otomatis. Harus tercakup persetujuan rencana atau diminta ulang. Sebelum kembali, periksa kondisi aktual dan pastikan ID asal belum dipakai orang lain, jalur fiber asal tersedia serta backup dapat diterapkan. Jika registrasi baru perlu dihapus, tampilkan target tujuan secara eksplisit; jangan tertukar dengan perintah penghapusan asal.

Koordinasikan fiber kembali, hapus hanya binding baru yang memang dibuat oleh migrasi sesuai rencana, daftarkan kembali SN pada PON/ID asal, lalu pulihkan konfigurasi dari backup yang diverifikasi. Urutan detail mengikuti pembatasan duplikasi SN firmware. Verifikasi ulang seluruh layanan. Jika kapasitas/ID/kabel berubah atau rollback gagal, berhenti dan eskalasi; jangan menghapus ONU lain atau memperluas dampak.

## Pitfalls
- Hapus binding dapat menghapus konfigurasi terkait; tidak ada jaminan ONU otomatis membawa seluruh provisioning ke PON baru.
- Berpindah splitter dalam satu PON tidak sama dengan migrasi antar-PON.
- Discovery index bukan jaminan ID tujuan yang boleh dipakai.
- Profile dan VLAN global tidak boleh dihapus saat membersihkan binding pelanggan.
- Prosedur ini adalah komposisi registrasi/penghapusan/restore layanan, bukan command move vendor yang teruji.
- Tidak mengubah inventaris koneksi OLT/host hanya karena interface pelanggan berpindah.
