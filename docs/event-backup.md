# Private event preservation and reconstruction

Raw event data stays outside GitHub. System, audit and configuration-tracker events can contain account names, addresses and sensitive configuration values. Preserve originals in access-restricted storage and publish only reviewed summaries.

## Current capture

A census through the authenticated Search Head used:

```spl
| tstats count where (index=* OR index=_*) earliest=0 latest=1794004702 by index
```

The exclusive cutoff is **2026-11-06 22:38:22 UTC**. The [machine-readable expected counts](../evidence/validation/event-census-20261106.json) contain:

| Index | Expected events |
| --- | ---: |
| `_audit` | 186,253 |
| `_configtracker` | 1,526 |
| `_internal` | 4,718,065 |
| `_introspection` | 2,833,893 |
| `_telemetry` | 140 |
| `linux_os` | 957,264 |
| **Total** | **8,697,141** |

The original 3 November census contained 666,094 events. It was rechecked with identical results before preparing the expanded capture.

## Why the original JSON was rejected

The owner supplied a 17,498,112-byte JSON export on 2026-11-06. Verification read 13,371 complete records, then found truncated JSON. Its readable prefix contained 995 `_audit`, 7,734 `_internal`, 3,350 `_introspection` and 1,292 `linux_os` records. Required fields were present in that prefix, but the file did not contain the expected original dataset. The unchanged file and failed verification report remain private.

## Compressed server-side export

A 14-event trial confirmed that the installed `outputcsv` command writes a readable gzip-compressed CSV when given a `.csv.gz` filename. This preserves multiline event content and source metadata without a large uncompressed copy.

The expanded query was:

```spl
(index=* OR index=_*) earliest=0 latest=1794004702
| fields _raw _time _indextime host source sourcetype index splunk_server _cd _bkt
| outputcsv override_if_empty=false splunk_preserve_20261106T223822Z_all_c6b7f2.csv.gz
| stats count by index
```

The job used substantial temporary storage. It was finalized when the Search Head's free space fell below the planned margin. After finalization, Splunk reported all six expected counts and confirmed the output file. A “Partial results” job label is not enough to determine archive completeness: the archive itself must pass full decompression, field checks and exact per-index counts. The server verification completed on **2026-11-06 at 23:08:45 UTC**: **PASS, 8,697,141 records, no missing required fields, and successful gzip CRC/EOF validation**. The compressed archive is 1,315,156,954 bytes. Download and local hash verification remain pending; see the [preservation checklist](preservation-checklist.md).

The trailing `stats` was used to display counts. For a future export, consider ending the query at `outputcsv` and validating counts from the resulting file; the large combined search and result processing need a deliberate disk budget. Use unique filenames, bounded captures and access restrictions. Do not overwrite existing backup files or change production retention to free space.

[Splunk documents `outputcsv`](https://help.splunk.com/en/splunk-enterprise/spl-search-reference/10.0/search-commands/outputcsv) as a local Search Head export with no result-count limit. The command can add internal metadata fields and flattens multivalued fields. This capture selects original raw content and scalar source metadata; it is not a complete knowledge-object or bucket backup.

## Verify the downloaded file

Place the archive under the ignored `.recovery/event-export/` directory and run:

```sh
python3 scripts/verify_event_export.py \
  .recovery/event-export/splunk-preserve-all-events-20261106T223822Z.csv.gz \
  --expected evidence/validation/event-census-20261106.json \
  --report .recovery/event-export/local-verification.json
```

The verifier automatically recognizes `.csv.gz`; it also supports JSON export envelopes. It reads to EOF, checks gzip integrity, verifies required fields, compares exact counts by index and hashes the entire file. It fails on malformed/truncated data, preview JSON, missing fields or count mismatches. Reports contain counts and hashes, never raw event content.

Compare the downloaded SHA-256 with the server report. A server-side pass does not prove that a download completed. Keep an independent private copy and verify its hash before cloud retirement. The separate configuration archive does not include the full event export.

## Reconstruct for future practice

1. Build a separate supported environment using the [rebuild guide](rebuild.md), with fresh credentials and trust.
2. Keep the verified archive unchanged. Read a copy using a proper CSV parser with gzip and multiline support, or the verifier's `export_rows()` function. Preserve `_raw`, original event time, host, source, sourcetype and original index.
3. Load `linux_os` events into a new practice index. Put historical internal/audit/configuration events in separate archival practice indexes and retain their original index as metadata.
4. Explicitly map `_raw` to event content and the original timestamp and source metadata to the corresponding ingest fields. Preserve original `_indextime`, bucket IDs and search-server identity as archival metadata; they will not become the new installation's actual indexing time or storage identity.
5. Validate counts by original index, representative timestamps and fields, then rerun saved searches and the dashboard using absolute historical bounds. Record transformations and compare preserved raw content.

No full replay or restore has been executed. An event export does not preserve bucket structures, search jobs, KV Store, credentials, licenses, expired data or events outside the account's search permissions. Events after the cutoff are excluded. Byte-for-byte infrastructure restoration requires additional backup work and authorization for any cloud changes.
