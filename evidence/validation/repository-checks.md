# Repository checks

Last run locally on 2026-11-06 with Python 3.9.6. The same checks run in GitHub Actions.

| Check | Result | Scope |
| --- | --- | --- |
| `python3 -m unittest discover -s tests -v` | PASS, 18 tests | Collection boundaries, secret-store exclusions, symlinks, redaction syntax, version/address handling, provenance mismatches, dashboard syntax and private JSON/CSV-gzip export count, multiline preservation and truncation checks |
| `python3 scripts/check_repo.py` | PASS | Recognizable sensitive patterns, disallowed file types, local documentation links, reviewed image hashes, recovered artifact hashes, dashboard XML/JSON |
| `bash -n scripts/original/system_metrics.sh` | PASS | Shell syntax only; the recovered script was not executed locally |
| Screenshot review | PASS | Seven real captures reviewed; account/project/live-address details excluded |

These checks are separate from [live Splunk validation](../../docs/validation.md). They do not certify OS compatibility, secure transport, complete sensitive-data removal or restore success.

Custom credentials, inline structured fields, arguments, IPv6, free-form business content and filenames still require manual review. The collector is selective, and its scope is documented in the recovery runbook. Private event-export verification must use the actual downloaded file; synthetic tests do not prove that an export completed.
