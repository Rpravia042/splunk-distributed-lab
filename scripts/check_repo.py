#!/usr/bin/env python3
"""Check publishable working-tree files without displaying sensitive matches.

Does not scan Git history or certify safety. Raw private directories are skipped.
"""

import hashlib
from pathlib import Path
import re
import sys

from sanitize import EMAIL, PROVIDER_PATTERN

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', '.recovery', '__pycache__'}
BLOCKED_NAMES = {'splunk.secret', 'passwd', 'passwords.conf', 'user-seed.conf', '.env'}
BLOCKED_SUFFIXES = {'.pem', '.key', '.p12', '.pfx', '.lic', '.tar', '.tgz', '.zip', '.log'}
TEXT_SUFFIXES = {'.md', '.py', '.sh', '.conf', '.json', '.yaml', '.yml', '.spl', '.txt'}


def issues_for_text(text):
    checks = {
        'private key': r'-----BEGIN (?:[A-Z]+ )?PRIVATE KEY-----',
        'Splunk encrypted value': r'\$[147]\$[^\s\"\x27,;]{8,}',
        'SSH key': r'(?m)^(?:ssh-(?:rsa|ed25519)|ecdsa-sha2-\S+)\s+[A-Za-z0-9+/=]{30,}',
        'credential-bearing URL': r'https?://[^\s/@]+:[^\s/@]+@',
        'cloud project identifier': r'project-[a-f0-9]{8}-[a-f0-9-]{8,}',
        'IPv4 address': r'(?<![\w.])(?:\d{1,3}\.){3}\d{1,3}(?![\w.])',
    }
    issues = [name for name, pattern in checks.items() if re.search(pattern, text)]
    if PROVIDER_PATTERN.search(text):
        issues.append('provider token')
    if EMAIL.search(text):
        issues.append('email address')
    # Entire-line assignment check for config, shell and ordinary JSON/YAML keys.
    for line in text.splitlines():
        if line.lstrip().startswith('#'):
            continue
        match = re.match(r'''\s*(?:export\s+)?["']?([\w.-]*(?:password|passwd|pass4SymmKey|secret|token|credential|api[_-]?key)[\w.-]*)["']?\s*[:=]\s*(.*)$''', line, re.I)
        if match:
            value = match[2].strip().strip(',').strip('\"\x27')
            if match[1].lower() == 'persist-credentials' and value == 'false':
                continue  # GitHub checkout's credential-storage switch, not a secret.
            if value and not value.startswith(('[REDACTED', '<REDACTED')):
                issues.append('sensitive assignment')
    return sorted(set(issues))


def main():
    errors = []
    reviewed_images = {}
    hashfile = ROOT / 'evidence/SHA256SUMS'
    if hashfile.exists():
        for line in hashfile.read_text().splitlines():
            digest, name = line.split('  ', 1)
            reviewed_images[name] = digest
    for path in sorted(ROOT.rglob('*')):
        rel = path.relative_to(ROOT)
        if any(part in SKIP for part in rel.parts):
            continue
        if path.is_symlink():
            errors.append((str(rel), 'symlink requires review'))
            continue
        if not path.is_file():
            continue
        if path.name in BLOCKED_NAMES or path.suffix.lower() in BLOCKED_SUFFIXES or path.name.startswith('.env.'):
            errors.append((str(rel), 'blocked file type/name'))
            continue
        if path.suffix.lower() == '.jpg':
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            if reviewed_images.get(str(rel)) != digest:
                errors.append((str(rel), 'image has no matching reviewed hash'))
            continue
        if path.suffix not in TEXT_SUFFIXES and path.name not in {'.gitignore', 'SHA256SUMS'}:
            errors.append((str(rel), 'unreviewed file type'))
            continue
        try:
            text = path.read_text(encoding='utf-8')
        except UnicodeError:
            errors.append((str(rel), 'non-UTF-8 text'))
            continue
        for reason in issues_for_text(text):
            errors.append((str(rel), reason))
        if path.suffix == '.md':
            for target in re.findall(r'\]\(([^)]+)\)', text):
                if '://' in target or target.startswith('#'):
                    continue
                if not (path.parent / target.split('#')[0]).exists():
                    errors.append((str(rel), 'missing local link target'))
    for name, reason in errors:
        print(f'{name}: {reason}')
    if errors:
        print(f'FAIL: {len(errors)} findings; values intentionally omitted.')
        return 1
    print('PASS: repository checks. Manual review and history review are still required.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
