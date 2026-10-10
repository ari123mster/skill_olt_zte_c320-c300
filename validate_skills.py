"""Offline structural and coverage checks; no device commands executed."""
from pathlib import Path
import re
import sys

root = Path(__file__).resolve().parent
failures = []


def check(condition, message):
    """Collect failures instead of assert so python -O cannot silence checks."""
    if not condition:
        failures.append(str(message))


def read(path):
    # Tolerate CRLF from core.autocrlf checkouts; .gitattributes pins LF but older clones may differ.
    return path.read_text(encoding='utf-8').replace('\r\n', '\n')


expected = {
    'zte-olt-onu-diagnostics', 'zte-olt-onu-config-audit',
    'zte-olt-onu-access-management', 'zte-olt-onu-lifecycle',
    'zte-olt-system-health', 'zte-olt-uplink-vlan-operations',
    'zte-olt-bootstrap-management', 'zte-olt-gpon-profiles',
    'zte-olt-vlan-provisioning', 'zte-olt-onu-provisioning',
    'zte-olt-onu-trunking', 'zte-olt-onu-wan-web',
    'zte-olt-onu-serial-replacement', 'zte-olt-onu-tr069-acs',
    'zte-olt-clock-ntp', 'zte-olt-snmp-management',
    'zte-olt-admin-ssh', 'zte-olt-onu-decommission',
    'zte-olt-connection-inventory', 'zte-olt-onu-pon-migration',
}
files = sorted(root.glob('*/SKILL.md'))
check({p.parent.name for p in files} == expected, 'Skill set mismatch')
readme = read(root / 'README.md')
texts = []
for path in files:
    text = read(path)
    check(text.startswith('---\n'), path)
    parts = text[4:].split('\n---\n', 1)
    if len(parts) != 2:
        check(False, (path, 'frontmatter not closed'))
        continue
    front, body = parts
    name_m = re.search(r'^name: (.+)$', front, re.M)
    desc_m = re.search(r'^description: (.+)$', front, re.M)
    if not name_m or not desc_m:
        check(False, (path, 'missing name/description'))
        continue
    name, desc = name_m.group(1), desc_m.group(1)
    check(name == path.parent.name and re.fullmatch(r'[a-z0-9-]{1,64}', name), path)
    check(0 < len(desc) <= 60 and desc.endswith('.'), (path, desc))
    check(': ' not in desc, (path, 'Unquoted YAML description colon'))
    check('platforms: [linux, macos, windows]' in front, path)
    check(body.strip() and len(text) < 100000, path)
    for section in ('## Kapan Digunakan', '## Pitfalls', '## Verifikasi', '## Prasyarat dan pengaman'):
        check(section in body, (path, section))
    check(re.search(r'^## (Pengaman|Batas penggunaan|Prasyarat)$', body, re.M) is None, (path, 'legacy safety heading; use "## Prasyarat dan pengaman"'))
    check(re.search(r'^metadata:\n  hermes:\n    tags: \[.+\]\n    related_skills: \[.+\]$', front, re.M), (path, 'metadata.hermes tags/related_skills'))
    check(not re.search(r'\n{3,}', text) and text.endswith('\n') and not text.endswith('\n\n'), (path, 'blank-line runs or trailing whitespace'))
    check(text.count('```') % 2 == 0, (path, 'unbalanced fences'))
    check(name in readme, ('README missing', name))
    check('## Persetujuan pengguna untuk eksekusi berisiko' in body, path)
    check('Diam atau jawaban ambigu bukan persetujuan.' in body, path)
    # Ambiguous mode line must stay out of executable blocks (see lifecycle/access-management notes).
    check(not re.search(r'^pon-onu$', body, re.M), (path, 'bare pon-onu line in command block'))
    # Every references/<file> mentioned must exist next to the skill.
    for ref in set(re.findall(r'references/[A-Za-z0-9_.-]+', body)):
        check((path.parent / ref).is_file(), (path, 'missing', ref))
    texts.append(text)
    print('PASS', name)
combined = '\n'.join(texts)
for command in (
    'show gpon onu uncfg', 'show gpon remote-onu interface wifi',
    'show gpon remote-onu model', 'registration-method sn <NEW_SN>',
    'show processor', 'show temperature', 'restore factory',
    'reset-card slotno', 'swap', 'show interface optical-module-info',
    'profile tcont', 'onu-profile gpon line', 'onu-profile gpon remote',
    'security-mgmt', 'wan-ip 1 mode pppoe', 'show run section | include',
    'set-pnp enable', 'show pon power attenuation', 'dhcp-enable false',
):
    check(command in combined, ('Missing command coverage', command))
provisioning = read(root / 'zte-olt-onu-provisioning/SKILL.md')
acs = read(root / 'zte-olt-onu-tr069-acs/SKILL.md')
check('Mau ditambah TR-069/ACS atau tidak?' in provisioning, 'provisioning ACS question')
check('Belum dijawab: tunggu' in provisioning, 'provisioning wait rule')
for question in ('Mode bridge mau access atau trunk?', 'VLAN berapa yang mau diaktifkan?', 'Mau dipasang di port eth berapa saja?'):
    check(question in provisioning, question)
check('tr069-mgmt <TR069_ID> acs <ACS_URL>' in acs, 'acs template')
check('Inform terbaru' in acs, 'acs verification')
migration = read(root / 'zte-olt-onu-pon-migration/SKILL.md')
for required in ('## Rollback', '## Rencana dan titik persetujuan', 'no onu <OLD_ONU_ID>', 'Jangan menghapus registrasi lama sebelum'):
    check(required in migration, required)
check('## Batas sementara: hanya pelanggan PPPoE' in migration, 'migration scope')
check('PPPoE yang diterminasi di router pelanggan melalui ONT bridge tetap termasuk bridge' in migration, 'migration bridge rule')
catalog = read(root / 'zte-olt-gpon-profiles/references/onu-type-catalog.md')
catalog_types = set(re.findall(r'^\s*onu-type ([A-Za-z0-9_-]+) gpon', catalog, re.M))
check(len(catalog_types) == 20, ('catalog expects 20 onu-type names, found', len(catalog_types)))

if failures:
    for failure in failures:
        print('FAIL', failure)
    sys.exit(f'{len(failures)} check(s) failed')
print(f'PASS: {len(files)} skills; frontmatter subset, sections, fences, references, catalog and command coverage.')
print('Offline only: no firmware or live-device validation.')
