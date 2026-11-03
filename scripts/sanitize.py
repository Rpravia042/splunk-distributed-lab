#!/usr/bin/env python3
"""Create a candidate text copy for MANUAL review, never publication approval."""

import argparse
import ipaddress
import json
from pathlib import Path
import re
import sys

SENSITIVE_FIELD = r'(?:[\w.-]*(?:password|passwd|pass4SymmKey|secret|token|api[_-]?key|credential)[\w.-]*)'
ASSIGNMENT = re.compile(r'(?im)^(\s*(?:export\s+)?[\"\x27]?' + SENSITIVE_FIELD + r'[\"\x27]?\s*[:=]\s*).*$')
PRIVATE_BLOCK = re.compile(r'-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----', re.S)
SSH_KEY = re.compile(r'(?m)^(?:ssh-(?:rsa|ed25519)|ecdsa-sha2-\S+)\s+\S+.*$')
EMAIL = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b')
IPV4 = re.compile(r'(?<![\w.])(?:\d{1,3}\.){3}\d{1,3}(?:/\d{1,2})?(?![\w.])')
PROVIDER_PATTERN = re.compile(r'\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|AIza[A-Za-z0-9_-]{25,}|AKIA[A-Z0-9]{16})\b')


def sanitize(text, replacements=None):
    text = PRIVATE_BLOCK.sub('[REDACTED_PRIVATE_KEY]', text)
    text = SSH_KEY.sub('[REDACTED_SSH_KEY]', text)
    text = ASSIGNMENT.sub(lambda m: m.group(1) + '[REDACTED]', text)
    text = re.sub(r'(?i)(Authorization\s*[:=]\s*(?:Bearer|Basic)\s+)\S+', r'\1[REDACTED]', text)
    text = re.sub(r'(https?://)[^\s/@]+:[^\s/@]+@', r'\1[REDACTED]@', text)
    text = re.sub(r'\$[147]\$[^\s\"\x27,;]+', '[REDACTED_SPLUNK_VALUE]', text)
    text = PROVIDER_PATTERN.sub('[REDACTED_TOKEN]', text)
    text = EMAIL.sub('[REDACTED_EMAIL]', text)

    def redact_ip(match):
        value = match.group().split('/')[0]
        try:
            ipaddress.ip_address(value)
        except ValueError:
            return match.group()
        return '[REDACTED_IPV4]'

    text = IPV4.sub(redact_ip, text)
    for original, replacement in sorted((replacements or {}).items(), key=lambda item: -len(item[0])):
        text = text.replace(original, replacement)
    return text


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('destination', type=Path)
    parser.add_argument('--map', dest='mapping', type=Path)
    args = parser.parse_args()
    try:
        replacements = json.loads(args.mapping.read_text()) if args.mapping else {}
        if (not isinstance(replacements, dict) or any(
                not isinstance(k, str) or not k or not isinstance(v, str)
                for k, v in replacements.items())):
            raise ValueError('Invalid replacement map')
        source = args.source.read_text(encoding='utf-8')
        if '\x00' in source:
            raise ValueError('Binary input is unsupported')
        args.destination.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        # Exclusive creation also prevents following an existing destination symlink.
        import os
        fd = os.open(args.destination, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, 'w', encoding='utf-8') as stream:
            stream.write(sanitize(source, replacements))
    except (OSError, ValueError, UnicodeError):
        print('Sanitization failed: check UTF-8 input, map and non-existing destination.', file=sys.stderr)
        return 1
    print('Candidate created. Review all content, custom secrets, IPv6, identifiers and filenames manually.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
