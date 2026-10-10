"""LEGACY, one-time conversion of the EMPTY Password-column template; no secret extraction.

Already applied to this package (see MIGRASI.md "Status awal"). New workbooks come from
create_inventory_template.py with the Credential_Ref schema; keep this only for old copies.
"""
from pathlib import Path
import os
import tempfile
from openpyxl import load_workbook
root = Path(__file__).resolve().parent
path = root / 'olt_connections.xlsx'
original = path.read_bytes()
wb = load_workbook(path)
ws = wb['OLT']
# Plain if/raise, not assert: these guards must survive python -O.
if ws['G1'].value not in ('Password', 'Credential_Ref'):
    raise SystemExit('Unexpected schema')
if any(c.value is not None for row in ws.iter_rows(min_row=2) for c in row):
    raise SystemExit('Nonempty workbook: migrate credentials manually before conversion')
ws['G1'] = 'Credential_Ref'
ws.column_dimensions['G'].width = 32
notes = wb['Petunjuk']
notes.delete_rows(1, notes.max_row)
for text in [
    'INVENTARIS OLT - Excel metadata, password hanya di KeePassXC.',
    'Credential_Ref: OLT/<OLT_ID>, sesuai entry unik pada grup OLT di vault.',
    'Vault: olt_credentials.kdbx di folder paket. Pengguna membuatnya sendiri di KeePassXC.',
    'Jangan menyimpan password, master passphrase atau key file dalam Excel/folder paket.',
    'SSH/TELNET, port 1-65535. Konfirmasi port aktual.',
    'Ikuti MIGRASI.md untuk pemindahan Windows/Linux; path relatif.',
    'Tidak ada koneksi otomatis atau profil contoh.'
]: notes.append([text])
fd, tmp = tempfile.mkstemp(suffix='.xlsx', dir=root)
os.close(fd)
try:
    wb.save(tmp)
    check = load_workbook(tmp)
    ok = (
        check['OLT']['G1'].value == 'Credential_Ref'
        and len(check['OLT'].data_validations.dataValidation) == 2
        and all(c.value is None for row in check['OLT'].iter_rows(min_row=2) for c in row)
    )
    check.close()
    wb.close()
    if not ok:
        raise SystemExit('Converted workbook failed verification')
    if path.read_bytes() != original:
        raise SystemExit('Workbook changed during update')
    os.replace(tmp, path)
finally:
    if os.path.exists(tmp): os.unlink(tmp)
print('PASS: empty workbook migrated; Credential_Ref column; no passwords; 2 validation rules.')
