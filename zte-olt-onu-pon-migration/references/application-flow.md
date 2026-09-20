# Hasil inspeksi statis aplikasi olt-mikrotik

Referensi lokal relatif root aplikasi; bukan command yang boleh dieksekusi otomatis. Tidak membaca .env, database aktual atau password perangkat; tidak mengubah aplikasi.

## Jalur yang ditelusuri
- routes/web.php sekitar 344–361: migrate, save-migrate dan getCustomerMigrate menunjuk ConnectionController.
- resources/views/v/olt/migrate.blade.php: pilihan source/destination, GET cekPort dan getCustomerMigrate, POST saveMigrate, payload parallel arrays.
- app/Http/Controllers/ConnectionController.php:
  - 850–934 getCustomerMigrate: membaca interface ONU + ONU running config; metadata dan password PPPoE dikirim ke frontend.
  - 938–1028 saveMigrate: validasi VLAN integer tunggal; koneksi ke OLT tujuan; registrasi dan provisioning PPPoE.
  - 1573–1598 cekPort: show run interface gpon-olt_<port>, filter/format baris.
  - 4505–4537 outMigrate, outMigrateSave, migrate: halaman hasil, update DB pelanggan terpisah, daftar OLT tujuan.
  - 4553–4576 telnetConnect: host/port record OLT, fallback port 23, decrypt username/password via Laravel Crypt; prompt #. terminal length 0 hanya jika flag diaktifkan (cekPort).
  - 4903–4908 telnetDisconnect: disconnect saja, bukan write/commit.
  - 5645–5657 extractPppoeCredentials: mengambil WAN PPPoE pertama dengan token non-whitespace; bukan parser seluruh layanan.
- resources/views/v/olt/outMigrate.blade.php: tombol Update DataBase mengirim customer_id, port dan olt_id sebagai hidden fields.

Nomor baris adalah posisi saat inspeksi; bisa berubah. Tidak menelusuri implementasi C600 karena di luar cakupan skill. Library transport, middleware keseluruhan, AuditLogger, schema/constraint database dan endpoint lain belum diaudit menyeluruh; jangan menyatakan sistem aman atau validasi server sepenuhnya tidak ada berdasarkan review terbatas ini.

## Perilaku penting
saveMigrate menggunakan OLT tujuan dari oltHidden. Parameter id sumber dipakai untuk redirect, bukan menghapus binding lama. Tidak ada no onu sumber pada method ini. Tidak ada rollback perangkat atau transaksi yang terlihat dalam method tersebut. Bila ONU kedua gagal, ONU pertama dapat sudah berubah.

Registrasi memakai ONU-type ALL, T-CONT profile 1G, GEM 1, satu service VLAN identik user/network, WAN PPPoE dengan VLAN profile V<VLAN>. Nama/deskripsi ditulis dari input. WAN ping/traceroute serta web dan Telnet diaktifkan. Ini template PPPoE opinionated, bukan salinan konfigurasi sumber. Skill tidak mengadopsi default ini.

Hanya respons registrasi indeks 1 dibandingkan string Successful; respons konfigurasi berikutnya tidak diperiksa dalam method. Session outMigrate dan toast sukses bukan bukti layanan end-to-end. Tidak ada write di method atau disconnect helper yang dibaca.

outMigrateSave melakukan update customers berdasarkan customer_id ke olt_id/port. Tidak terlihat pembatas lokasi asal atau pemeriksaan affected-row count dalam method; keunikan customer_id secara global belum diverifikasi schema. Update database adalah tahap terpisah dari konfigurasi perangkat.

## Validasi tambahan yang wajib di skill
- Setiap array SN/ID/nama/deskripsi/customer harus lengkap dan pasangan tetap cocok. Backend yang dibaca hanya membandingkan panjang username/password dengan no_onu; jangan anggap seluruh payload terjamin.
- Target/port/ONU ID/SN dan teks yang menjadi CLI harus divalidasi; jangan merangkai input mentah menjadi command.
- Discovery hasil parser/halaman dapat tidak lengkap: regex tipe menggunakan word characters dan prompt filter spesifik; tidak menjamin semua variasi firmware tercakup.
- Data getCustomerMigrate dikunci hanya oleh suffix ONU ID, sehingga jangan menggabungkan multi-PON menggunakan key itu. Gunakan identitas OLT+PON+ONU_ID+SN.
- Metadata description diambil lewat pencarian substring; cocokkan deskripsi tingkat interface agar tidak tertukar service-port description.
- Kredensial PPPoE tidak boleh masuk model/log/DOM yang dibagikan. Parser pertama tidak membuktikan seluruh WAN sudah disalin.
- Refresh snapshot sebelum cutover dan cek ID kosong aktual. Jangan memakai rentang generator 1–1000 sebagai batas perangkat.
- Hasil register, layanan, write, DB update dan cleanup sumber harus dicatat terpisah.

## Batas penggunaan
Temuan ini untuk memperkuat skill, bukan laporan pengujian aplikasi. Belum ada koneksi OLT, perubahan database atau eksekusi endpoint. Command transport Telnet aplikasi tidak membuktikan dukungan SSH; skill inventory tetap memisahkan pilihan protocol pengguna.
