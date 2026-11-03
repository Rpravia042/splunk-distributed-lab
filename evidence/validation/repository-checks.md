# Repository checks

Run locally on 2026-11-03 with Python 3.9.6.

| Check | Result | Scope |
| --- | --- | --- |
| `python3 -m unittest discover -s tests -v` | PASS, 8 tests | Synthetic sanitizer tests, safe overwrite refusal, bounded collection, excluded secret stores and symlink rejection |
| `python3 scripts/check_repo.py` | PASS | Recognizable sensitive patterns, disallowed files, local documentation links and reviewed screenshot hashes |
| Screenshot review | PASS | VM and firewall crops visually inspected; account, project and live-address details excluded |

These results do not demonstrate guest recovery, Splunk compatibility, forwarding, search success, secure transport or a successful restore. All live checks remain pending in [the validation matrix](../../docs/validation.md).

The sanitizer has known limits: custom credentials, inline structured fields, command arguments, IPv6, free-form business data and filenames require manual review. The collector is bounded and selective; every skipped or unreadable file must be considered before declaring preservation complete.
