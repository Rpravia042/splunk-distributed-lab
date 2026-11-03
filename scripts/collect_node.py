#!/usr/bin/env python3
"""Stream a bounded PRIVATE file collection to stdout; never run Splunk.

Run via an already-authorized SSH connection. This is not a full system backup.
"""

import argparse
import datetime
import hashlib
import io
import json
import os
from pathlib import Path
import stat
import sys
import tarfile

ALLOWED_SUFFIXES = {'.conf', '.xml', '.json', '.yaml', '.yml', '.sh', '.py',
                    '.pl', '.js', '.css', '.html', '.csv', '.md', '.txt'}
EXCLUDED_DIRS = {'auth', 'licenses', 'license', '.git', '__pycache__', 'node_modules'}
EXCLUDED_NAMES = {'splunk.secret', 'passwd', 'passwords.conf', 'user-seed.conf',
                  '.ui_login', '.splunk', 'server.pem'}


def selected(path):
    """Allow useful text/config types, explicitly excluding known secret stores."""
    return (path.name.lower() not in EXCLUDED_NAMES
            and not any(p.lower() in EXCLUDED_DIRS for p in path.parts)
            and (path.suffix.lower() in ALLOWED_SUFFIXES or path.name == 'splunk.version'))


def collect(home, output, max_file=5 * 1024 * 1024, max_total=100 * 1024 * 1024):
    home = Path(home)
    root = home / 'etc'
    if not root.is_dir() or home.is_symlink() or root.is_symlink():
        raise ValueError('Expected a real Splunk installation with an etc directory')
    report = {'captured_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'scope': 'selected files under Splunk etc; not a complete backup',
              'files': [], 'skipped': [], 'errors': []}
    total = 0

    def walk_error(error):
        report['errors'].append({'path': str(error.filename), 'reason': 'directory unreadable'})

    with tarfile.open(fileobj=output, mode='w|') as archive:
        for current, dirs, names in os.walk(root, followlinks=False, onerror=walk_error):
            for name in sorted(dirs[:]):
                path = Path(current) / name
                if name.lower() in EXCLUDED_DIRS or path.is_symlink():
                    dirs.remove(name)
                    report['skipped'].append({'path': str(path.relative_to(home)),
                                              'reason': 'excluded directory or symlink'})
            dirs.sort()
            for name in sorted(names):
                path = Path(current) / name
                rel = path.relative_to(home).as_posix()
                if not selected(path.relative_to(home)):
                    report['skipped'].append({'path': rel, 'reason': 'type or secret-store exclusion'})
                    continue
                fd = None
                try:
                    # O_NOFOLLOW rejects leaf symlinks; O_NONBLOCK avoids hanging on special files.
                    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
                    info = os.fstat(fd)
                    if not stat.S_ISREG(info.st_mode):
                        report['skipped'].append({'path': rel, 'reason': 'not a regular file'})
                        continue
                    if info.st_size > max_file or total + info.st_size > max_total:
                        report['skipped'].append({'path': rel, 'reason': 'size limit'})
                        continue
                    with os.fdopen(fd, 'rb') as stream:
                        fd = None
                        data = stream.read(max_file + 1)
                    if len(data) > max_file or total + len(data) > max_total:
                        report['skipped'].append({'path': rel, 'reason': 'size changed during read'})
                        continue
                    member = tarfile.TarInfo(rel)
                    member.size = len(data)
                    member.mode = 0o600
                    member.mtime = int(info.st_mtime)
                    archive.addfile(member, io.BytesIO(data))
                    total += len(data)
                    report['files'].append({'path': rel, 'bytes': len(data),
                                            'sha256': hashlib.sha256(data).hexdigest()})
                except OSError:
                    report['errors'].append({'path': rel, 'reason': 'read failed; inspect permissions or links'})
                finally:
                    if fd is not None:
                        os.close(fd)
        report['included_bytes'] = total
        payload = (json.dumps(report, indent=2) + '\n').encode()
        member = tarfile.TarInfo('collection-report.json')
        member.size, member.mode = len(payload), 0o600
        archive.addfile(member, io.BytesIO(payload))
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('splunk_home', type=Path)
    args = parser.parse_args()
    try:
        report = collect(args.splunk_home, sys.stdout.buffer)
    except (ValueError, OSError) as error:
        print(type(error).__name__ + ': collection could not complete', file=sys.stderr)
        return 1
    print(f"Collected {len(report['files'])} files; {len(report['skipped'])} skipped; "
          f"{len(report['errors'])} read errors. PRIVATE output: review the report.", file=sys.stderr)
    return 2 if report['errors'] or not report['files'] else 0


if __name__ == '__main__':
    sys.exit(main())
