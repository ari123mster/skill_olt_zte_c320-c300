# Instalasi olt-agent pada Windows / Linux

Dokumen ini panduan untuk dijalankan kemudian. Jangan membuat profile, mengimpor file, menguji model atau menghubungkan OLT hanya karena membaca dokumen. Tunggu pengguna meminta instalasi. Pengujian perangkat ditunda sampai ada izin terpisah.

## 1. Buat profile baru terlebih dahulu

Hermes harus sudah terpasang. Jalankan dari CMD, PowerShell atau terminal Linux:

```text
hermes profile create olt-agent --no-skills --description "Asisten khusus OLT ZTE C300/C320; tindakan berisiko wajib persetujuan pengguna."
hermes profile show olt-agent
```

Jangan gunakan --clone atau --clone-all: profile ini tidak perlu mewarisi memory, SOUL, kredensial dan skill umum profile lain. --no-skills membuat profile tanpa bundled skills dan menonaktifkan sinkronisasi bundled skills untuk profile tersebut. Jika versi Hermes belum mendukung flag ini, berhenti dan cek dokumentasi/upgrade; jangan menghapus skill profile lain.

Jika olt-agent sudah ada, berhenti. Jangan hapus/recreate atau menimpa isinya tanpa izin dan backup. Jangan menjalankan `hermes profile use olt-agent`: default profile pengguna tidak perlu berubah.

## 2. Siapkan command olt-agent

Pembuatan profile normal juga membuat wrapper command. Jika alias belum dibuat:

```text
hermes profile alias olt-agent --name olt-agent
```

Pastikan lokasi wrapper yang ditampilkan Hermes ada di PATH. Buka terminal baru setelah PATH berubah. Untuk CMD/PowerShell cek `where.exe olt-agent`; Linux `command -v olt-agent`. Jangan membuat wrapper hardcoded berisi credential.

Jika alias belum dikenali, gunakan bentuk resmi sementara:

```text
hermes -p olt-agent chat
```

Perintah chat di atas hanya contoh cara akses; jangan dijalankan selama tahap import. Hasil akhir yang diinginkan adalah `olt-agent chat`.

## 3. Tentukan path profile aktual

Baca Path/Home dari `hermes profile show olt-agent`. Jangan menebak dari hostname atau profile aktif. Instalasi Windows ini biasanya memakai `%LOCALAPPDATA%\hermes\profiles\olt-agent`; Linux biasanya `~/.hermes/profiles/olt-agent`. HERMES_HOME/custom installation dapat mengubah lokasi tersebut.

Isi variabel tujuan di contoh berikut dengan path aktual. Source adalah folder paket ini. Semua command harus memakai quote karena nama folder mengandung `&`.

### 3a. Pastikan workbook inventaris ada di folder paket

`olt_connections.xlsx` sengaja tidak di-commit (`*.xlsx` ada di .gitignore), jadi clone baru tidak memilikinya dan script 4A/4B akan berhenti saat menyalinnya. Jika file belum ada, buat template kosong dulu dari folder paket (butuh Python + openpyxl):

```text
python create_inventory_template.py
```

Script menolak menimpa workbook yang sudah ada. Jangan mengisi profil atau password pada tahap ini; ikuti MIGRASI.md setelah instalasi.

## 4A. Windows: impor SOUL dan skill melalui PowerShell

Jika memakai CMD, jalankan `powershell` terlebih dahulu lalu gunakan blok PowerShell ini. Ganti nilai $dst bila hasil profile show berbeda. Jangan menjalankan profile selama penyalinan.

```powershell
$ErrorActionPreference = 'Stop'
$src = 'D:\skill_olt_zte_c320&c300'
$dst = Join-Path $env:LOCALAPPDATA 'hermes\profiles\olt-agent'

if (-not (Test-Path -LiteralPath $dst -PathType Container)) { throw 'Profile tidak ditemukan; cek hermes profile show olt-agent' }
if (-not (Test-Path -LiteralPath (Join-Path $src 'SOUL.md'))) { throw 'SOUL sumber tidak ditemukan' }
if (-not (Test-Path -LiteralPath (Join-Path $src 'olt_connections.xlsx'))) { throw 'olt_connections.xlsx belum ada; jalankan create_inventory_template.py dulu (langkah 3a)' }
$skills = @(Get-ChildItem -LiteralPath $src -Directory | Where-Object { $_.Name -like 'zte-olt-*' -and (Test-Path -LiteralPath (Join-Path $_.FullName 'SKILL.md')) })
if ($skills.Count -ne 20) { throw 'Jumlah skill bukan 20; periksa versi paket sebelum melanjutkan' }
$skillRoot = Join-Path $dst 'skills'
New-Item -ItemType Directory -Force -Path $skillRoot | Out-Null
if (@(Get-ChildItem -LiteralPath $skillRoot -Force).Count -gt 0) { throw 'Folder skills tujuan tidak kosong; jangan timpa tanpa review' }
$soulDest = Join-Path $dst 'SOUL.md'
if (Test-Path -LiteralPath $soulDest) {
    $backup = Join-Path $dst 'SOUL.before-olt-install.md'
    if (Test-Path -LiteralPath $backup) { throw 'Backup SOUL sudah ada; berhenti agar tidak tertimpa' }
    Copy-Item -LiteralPath $soulDest -Destination $backup
}
Copy-Item -LiteralPath (Join-Path $src 'SOUL.md') -Destination $soulDest
foreach ($skill in $skills) { Copy-Item -LiteralPath $skill.FullName -Destination $skillRoot -Recurse }
foreach ($name in @('olt_connections.xlsx', 'MIGRASI.md', 'validate_skills.py', 'README.md', '.gitignore')) {
    Copy-Item -LiteralPath (Join-Path $src $name) -Destination (Join-Path $skillRoot $name)
}
```

SOUL di root profile akan menjadi identitas profile; skill masuk folder skills profile, bukan profile default. Excel ditempatkan di root skills agar path relatif `../olt_connections.xlsx` dari skill inventory tetap benar.

## 4B. Linux: impor SOUL dan skill melalui Bash

Alternatif untuk Linux; jangan jalankan bagian Windows. Ganti $src sesuai lokasi paket dan $dst sesuai profile show.

```bash
set -e
src="$HOME/skill_olt_zte_c320&c300"
dst="$HOME/.hermes/profiles/olt-agent"

test -d "$dst" || { printf '%s\n' 'Profile tidak ditemukan'; exit 1; }
test -f "$src/SOUL.md" || { printf '%s\n' 'SOUL sumber tidak ditemukan'; exit 1; }
test -f "$src/olt_connections.xlsx" || { printf '%s\n' 'olt_connections.xlsx belum ada; jalankan create_inventory_template.py dulu (langkah 3a)'; exit 1; }
skills=()
for dir in "$src"/zte-olt-*; do
  if [ -d "$dir" ] && [ -f "$dir/SKILL.md" ]; then skills+=("$dir"); fi
done
[ "${#skills[@]}" -eq 20 ] || { printf '%s\n' 'Jumlah skill bukan 20; review paket'; exit 1; }
mkdir -p "$dst/skills"
shopt -s nullglob dotglob
existing=("$dst/skills"/*)
[ "${#existing[@]}" -eq 0 ] || { printf '%s\n' 'Folder skills tujuan tidak kosong'; exit 1; }
if [ -e "$dst/SOUL.md" ]; then
  [ ! -e "$dst/SOUL.before-olt-install.md" ] || { printf '%s\n' 'Backup SOUL sudah ada; berhenti agar tidak tertimpa'; exit 1; }
  cp -- "$dst/SOUL.md" "$dst/SOUL.before-olt-install.md"
fi
cp -- "$src/SOUL.md" "$dst/SOUL.md"
for dir in "${skills[@]}"; do cp -R -- "$dir" "$dst/skills/"; done
for name in olt_connections.xlsx MIGRASI.md validate_skills.py README.md .gitignore; do
  cp -- "$src/$name" "$dst/skills/$name"
done
```

Jika penyalinan gagal sebagian, jangan menghapus destination secara otomatis. Periksa file yang sudah tersalin dan lanjutkan melalui review/backup. Script sengaja menolak destination nonkosong saat dijalankan ulang.

## 5. Vault dan inventaris aktif

Import di atas menyalin workbook paket sebagai inventory profile. Setelah instalasi, inventory aktif berada di `<PROFILE_HOME>/skills/olt_connections.xlsx`. Jangan mengedit salinan sumber dan tujuan sekaligus lalu menganggap tersinkron.

Vault belum dibuat dalam paket awal. Buat melalui KeePassXC secara lokal pada `<PROFILE_HOME>/skills/olt_credentials.kdbx`, ikuti MIGRASI.md. Jika vault sudah dibuat pada paket, salin hanya setelah izin khusus pengguna dan pastikan tujuan belum ada:

PowerShell:
```powershell
$vaultDest = Join-Path $skillRoot 'olt_credentials.kdbx'
if (Test-Path -LiteralPath $vaultDest) { throw 'Vault tujuan sudah ada' }
Copy-Item -LiteralPath (Join-Path $src 'olt_credentials.kdbx') -Destination $vaultDest
```

Bash:
```bash
[ ! -e "$dst/skills/olt_credentials.kdbx" ] || exit 1
cp -- "$src/olt_credentials.kdbx" "$dst/skills/olt_credentials.kdbx"
```

Jangan menyalin master passphrase atau key file ke folder profile/paket. Jangan memasukkan rahasia ke chat/argument command. Batasi ACL/permission melalui prosedur OS yang disetujui. Backup/export profile dapat ikut membawa workbook/vault; perlakukan arsip sebagai data sensitif dan jangan publikasikan.

## 6. Konfigurasi model dan tools khusus profile

Setelah import dan bila pengguna meminta setup:

```text
olt-agent setup
olt-agent tools
```

Atur provider/model dan rahasia melalui mekanisme Hermes yang aman; jangan menyalin .env default sembarang. Jangan mengaktifkan YOLO atau bypass approval. Pilih tools minimum kebutuhan OLT. Jangan memakai --ignore-rules atau --safe-mode untuk sesi operasional: opsi tersebut dapat menonaktifkan injeksi SOUL/aturan.

## 7. Pemeriksaan file, bukan pengujian perangkat

Pemeriksaan statis opsional setelah import:

```text
olt-agent skills list
hermes profile show olt-agent
```

Windows PowerShell:
```powershell
python (Join-Path $skillRoot 'validate_skills.py')
if ((Get-FileHash -LiteralPath (Join-Path $src 'SOUL.md')).Hash -ne (Get-FileHash -LiteralPath $soulDest).Hash) { throw 'SOUL berbeda' }
```

Linux:
```bash
python3 "$dst/skills/validate_skills.py"
cmp -- "$src/SOUL.md" "$dst/SOUL.md"
```

Harus ada 20 skill, SOUL sumber/tujuan identik, dan profile yang dipakai olt-agent. Skill list tidak perlu chat/model atau koneksi OLT. Jika jumlah skill berubah pada versi paket mendatang, review manifest dan validator sebelum mengubah expected count.

## 8. Akses setelah pengguna siap

```text
olt-agent chat
```

Mulai sesi baru agar SOUL dan skill dimuat. Pengujian penolakan topik, model, koneksi dan perangkat hanya dilakukan kemudian atas permintaan pengguna. Tidak ada auto-test OLT pada instalasi ini.

SOUL adalah arahan perilaku, bukan firewall atau sandbox. Profile memisahkan state, bukan hak akses filesystem. Pembatasan OS/tool dan persetujuan tetap diperlukan. Jangan mengklaim topik di luar OLT mustahil dijawab hanya karena SOUL sudah dipasang.

## Referensi

https://hermes-agent.nousresearch.com/docs/user-guide/profiles
Command create/alias/show diverifikasi melalui help Hermes lokal saat penyusunan. Dokumen ini tidak menjalankan instalasi atau mengubah profile aktif.
