from pathlib import Path
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation

root = Path(__file__).resolve().parent
path = root / 'olt_connections.xlsx'
headers = ['OLT_ID', 'Nama_OLT', 'Host', 'Protocol', 'Port', 'Username', 'Credential_Ref', 'Catatan']
if path.exists():
    raise SystemExit('Refusing to overwrite existing credential workbook')
wb = Workbook()
ws = wb.active
ws.title = 'OLT'
ws.append(headers)
ws.freeze_panes = 'A2'
ws.auto_filter.ref = 'A1:H1001'
for cell in ws[1]:
    cell.font = Font(bold=True, color='FFFFFF')
    cell.fill = PatternFill('solid', fgColor='244062')
for col, width in zip('ABCDEFGH', [18, 25, 32, 16, 12, 25, 28, 45]):
    ws.column_dimensions[col].width = width
for row in ws.iter_rows(min_row=2, max_row=1001, max_col=8):
    for cell in row:
        cell.number_format = '0' if cell.column == 5 else '@'
protocol = DataValidation(type='list', formula1='"SSH,TELNET"', allow_blank=True)
port = DataValidation(type='whole', operator='between', formula1=1, formula2=65535, allow_blank=True)
for validation, area in [(protocol, 'D2:D1001'), (port, 'E2:E1001')]:
    validation.showErrorMessage = True
    validation.errorStyle = 'stop'
    validation.error = 'Protocol SSH/TELNET; port integer 1-65535.'
    ws.add_data_validation(validation)
    validation.add(area)
notes = wb.create_sheet('Petunjuk')
for value in [
    'INVENTARIS OLT - TEMPLATE KOSONG',
    'Password hanya di KeePassXC; Excel menyimpan Credential_Ref OLT/<OLT_ID>.',
    'Isi satu profil per baris. OLT_ID wajib unik.',
    'Host: IP/hostname tanpa protocol atau port. Port disimpan di kolom Port.',
    'Protocol SSH atau TELNET. SSH 22/Telnet 23 hanya port umum; konfirmasi port aktual.',
    'Isi password di KeePassXC lokal, bukan Excel/chat. Ikuti MIGRASI.md.',
    'Jangan membagikan, mengunggah, atau commit workbook ini.',
    'Kolom teks berformat Text. Jangan mengubah nilai input menjadi formula.',
    'Proteksi sheet/hidden column bukan enkripsi.',
    'Template tidak melakukan koneksi atau menyimpan akun contoh.',
]:
    notes.append([value])
notes.column_dimensions['A'].width = 110
# Exclusive creation prevents accidental replacement of existing credentials.
with path.open('xb') as stream:
    wb.save(stream)
check = load_workbook(path)
assert check.sheetnames == ['OLT', 'Petunjuk']
assert [c.value for c in check['OLT'][1]] == headers
assert all(c.value is None for row in check['OLT'].iter_rows(min_row=2) for c in row)
assert len(check['OLT'].data_validations.dataValidation) == 2
check.close()
print('PASS: workbook created, 0 profiles, 2 sheets, 8 columns, protocol/port validation.')
print(path)
