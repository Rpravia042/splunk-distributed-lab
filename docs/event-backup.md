# Private event preservation and reconstruction

Raw event data stays outside GitHub, including system, audit and configuration-tracker records. It can contain account names, addresses and sensitive configuration values. Preserve the original privately; publish only reviewed summaries.

## Capture scope

The observed event census used:

```spl
| tstats count where (index=* OR index=_*) earliest=0 latest=1793723730 by index
```

The exclusive cutoff is **2026-11-03 16:35:30 UTC**. Counts were:

| Index | Expected events |
| --- | ---: |
| `_audit` | 50,995 |
| `_configtracker` | 1,519 |
| `_internal` | 324,594 |
| `_introspection` | 157,957 |
| `_telemetry` | 14 |
| `linux_os` | 131,015 |
| **Total** | **666,094** |

The prepared export query is:

```spl
(index=* OR index=_*) earliest=0 latest=1793723730
| fields _raw _time _indextime host source sourcetype index splunk_server _cd _bkt
```

Splunk Web was set to JSON with Number of Results blank (all results). Its dialog stated that results beyond the stored artifact would rerun the search. Use fixed bounds and compare the resulting counts; a displayed search count or successful click does not prove a complete download. [Splunk export guidance](https://help.splunk.com/en/splunk-cloud-platform/search/search-manual/9.3.2411/export-search-results/export-data-using-splunk-web).

On 2026-11-06, the owner supplied a 17,498,112-byte JSON export. Verification found **13,371 complete records followed by truncated JSON**, compared with 666,094 expected events. The readable prefix contained 995 `_audit`, 7,734 `_internal`, 3,350 `_introspection` and 1,292 `linux_os` events. Required fields were present in those complete records. This is an incomplete export; the original file and verification report are preserved privately. Current status is tracked in the [preservation checklist](preservation-checklist.md).

## Verify locally

Place the downloaded file under the ignored, private `.recovery/event-export/` directory. Create an `expected-counts.json` object using the index names and counts above, then run:

```sh
python3 scripts/verify_event_export.py .recovery/event-export/events.json \
  --expected .recovery/event-export/expected-counts.json \
  --report .recovery/event-export/verification.json
```

The tool checks every JSON record, required event fields, exact counts by index and the file's SHA-256. It rejects malformed/truncated JSON and preview data, writes a private report without event content, and fails on mismatched counts. A pass establishes readability and agreement with this census, not a tested restore or absence of secrets.

Keep the export, report, configuration archive and original per-file hashes in access-restricted storage. Make an independent copy and verify its hash before any cloud retirement. The local configuration archive alone does not include the event export and is not an independent backup.

## Reconstruct for future practice

1. Build a separate supported Splunk environment using the [rebuild guide](rebuild.md). Generate fresh credentials and trust; do not install redacted server secrets.
2. Keep the downloaded JSON unchanged as the source of truth. Work from a copy. Preserve `_raw`, original event time, host, source, sourcetype and original index as event metadata when designing a replay.
3. Load `linux_os` events into a new practice index. For internal/audit/configuration events, use separate archival practice indexes and retain the original index as metadata; avoid mixing historical records with the new installation's operational indexes.
4. A JSON export envelope is not itself the original raw event. An import/replay process must explicitly map `_raw` to event content and the original timestamp and source metadata to their corresponding fields. The original `_indextime`, bucket IDs and search-server identity should be retained as archival metadata; they will not become the new installation's actual indexing time or storage identity.
5. Validate counts per original index, representative timestamps and fields, then rerun the saved searches and dashboard with absolute historical time bounds. Record any transformations and compare the preserved raw content.

No replay or full restore has been executed. An event export does not preserve Splunk bucket structures, search jobs, KV Store, credentials, licenses, expired data or events outside the account's search permissions. Events generated after the cutoff are excluded. If byte-for-byte infrastructure restoration is required, additional backup work and explicit authorization for any cloud changes are needed.
