"""Offline structural and coverage checks; no device commands executed."""
from pathlib import Path
import re

root = Path(__file__).resolve().parent
expected = {
    'zte-olt-onu-diagnostics', 'zte-olt-onu-config-audit',
    'zte-olt-onu-access-management', 'zte-olt-onu-lifecycle',
    'zte-olt-system-health', 'zte-olt-uplink-vlan-operations',
    'zte-olt-bootstrap-management', 'zte-olt-gpon-profiles',
    'zte-olt-vlan-provisioning', 'zte-olt-onu-provisioning',
    'zte-olt-onu-trunking', 'zte-olt-onu-wan-web',
    'zte-olt-onu-serial-replacement', 'zte-olt-onu-tr069-acs',
}
files = sorted(root.glob('*/SKILL.md'))
assert {p.parent.name for p in files} == expected, 'Skill set mismatch'
readme = (root / 'README.md').read_text(encoding='utf-8')
texts = []
for path in files:
    text = path.read_text(encoding='utf-8')
    assert text.startswith('---\n'), path
    front, body = text[4:].split('\n---\n', 1)
    name = re.search(r'^name: (.+)$', front, re.M).group(1)
    desc = re.search(r'^description: (.+)$', front, re.M).group(1)
    assert name == path.parent.name and re.fullmatch(r'[a-z0-9-]{1,64}', name), path
    assert 0 < len(desc) <= 60 and desc.endswith('.'), (path, desc)
    assert ': ' not in desc, 'Unquoted YAML description colon'
    assert 'platforms: [linux, macos, windows]' in front, path
    assert body.strip() and len(text) < 100000, path
    for section in ('## Kapan Digunakan', '## Pitfalls', '## Verifikasi', '## Sumber'):
        assert section in body, (path, section)
    assert text.count('```') % 2 == 0, path
    assert name in readme, ('README missing', name)
    assert re.search(r'https://(?:github\.com|pastebin\.com)/', body), path
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
    assert command in combined, ('Missing command coverage', command)
provisioning = (root / 'zte-olt-onu-provisioning/SKILL.md').read_text(encoding='utf-8')
acs = (root / 'zte-olt-onu-tr069-acs/SKILL.md').read_text(encoding='utf-8')
assert 'Mau ditambah TR-069/ACS atau tidak?' in provisioning
assert 'Belum dijawab: tunggu' in provisioning
assert 'tr069-mgmt <TR069_ID> acs <ACS_URL>' in acs
assert 'Inform terbaru' in acs
print(f'PASS: {len(files)} skills; frontmatter subset, sections, fences, catalog and command coverage.')
print('Offline only: no firmware or live-device validation.')
