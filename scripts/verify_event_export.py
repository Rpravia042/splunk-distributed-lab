#!/usr/bin/env python3
"""Verify a private Splunk JSON export without printing event content.

Accepts newline-delimited export envelopes, a JSON array, or a results envelope.
The expected JSON maps index names to counts measured with the same time bounds.
This verifies readability/counts/required fields, not restore fidelity or secret absence.
"""
import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import sys


def values(stream):
    decoder = json.JSONDecoder()
    buffer = ''
    done = False
    while True:
        buffer = buffer.lstrip()
        if buffer:
            try:
                value, end = decoder.raw_decode(buffer)
            except json.JSONDecodeError:
                if done:
                    raise ValueError('Invalid or truncated JSON') from None
            else:
                yield value
                buffer = buffer[end:]
                continue
        elif done:
            return
        chunk = stream.read(1024 * 1024)
        if not chunk:
            done = True
        buffer += chunk


def records(value):
    if isinstance(value, list):
        for item in value:
            yield from records(item)
    elif isinstance(value, dict):
        if value.get('preview') is True:
            raise ValueError('Preview data is not a final export')
        if 'result' in value:
            yield from records(value['result'])
        elif 'results' in value:
            yield from records(value['results'])
        elif '_raw' in value:
            yield value
        else:
            raise ValueError('Unknown JSON envelope; inspect privately')
    else:
        raise ValueError('Unexpected JSON value')


def verify(path, expected):
    counts = Counter()
    missing = Counter()
    parse_error = None
    if not expected or any(not isinstance(v, int) or v < 0 for v in expected.values()):
        raise ValueError('Expected counts must be a non-empty object of non-negative integers')
    with path.open(encoding='utf-8-sig') as stream:
        try:
            for value in values(stream):
                for row in records(value):
                    for key in ('_raw', '_time', 'host', 'source', 'sourcetype', 'index'):
                        if key not in row or row[key] is None or not isinstance(row[key], (str, int, float)):
                            missing[key] += 1
                    index = row.get('index')
                    if not isinstance(index, str):
                        missing['scalar_index'] += 1
                        continue
                    counts[index] += 1
        except ValueError as error:
            # Parser messages are fixed strings; never include raw event fragments.
            parse_error = str(error)
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    passed = dict(counts) == expected and not missing and parse_error is None
    return {'status': 'PASS' if passed else 'FAIL', 'events': sum(counts.values()),
            'counts': dict(sorted(counts.items())), 'expected': expected,
            'missing_or_invalid_fields': dict(missing), 'bytes': path.stat().st_size,
            'valid_complete_json': parse_error is None, 'parse_error': parse_error,
            'sha256': digest.hexdigest(),
            'limits': 'Count and readability check only; not a restore test or sensitive-data certification.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('export', type=Path)
    parser.add_argument('--expected', type=Path, required=True)
    parser.add_argument('--report', type=Path, required=True)
    args = parser.parse_args()
    try:
        expected = json.loads(args.expected.read_text())
        if not isinstance(expected, dict):
            raise ValueError('Invalid expected counts')
        report = verify(args.export, expected)
        fd = os.open(args.report, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, 'w') as stream:
            json.dump(report, stream, indent=2)
            stream.write('\n')
    except (OSError, ValueError, TypeError):
        print('Verification failed. Check input format, expected counts and unused report path privately.', file=sys.stderr)
        return 1
    print(f"{report['status']}: {report['events']} events; report written. No event content displayed.")
    return 0 if report['status'] == 'PASS' else 1


if __name__ == '__main__':
    sys.exit(main())
