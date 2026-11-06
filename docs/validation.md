# Validation results

Validated on **2026-11-03 UTC** after the owner authorized boot and temporary SSH access. Existing data was queried; no synthetic marker was injected. Counts describe fixed observations, not a continuously updated monitor.

| ID | Check | Result and evidence |
| --- | --- | --- |
| V01 | Version and service identity | **PASS**: Splunk 10.6.1.1, build `b2ae2962645c`, all nodes. SH/IDX `Splunkd.service` as `splunk`; UF `SplunkForwarder.service` as `splunkfwd`; all active/running. |
| V02 | Inputs and source access | **PASS**: all three UF monitor stanzas effective; service user can read all three sources. |
| V03 | Forwarding destination | **PASS**: effective target matches recovered output; established UF→IDX TCP 9997 connection seen at both ends. |
| V04 | Receiver | **PASS**: effective `[splunktcp://9997]`, listener and indexed events. |
| V05 | Index routing | **PASS**: effective `linux_os` paths and events returned from that index. No retention or durability guarantee tested. |
| V06 | Distributed search | **PASS**: sole peer `splunk-idx` Up, replication Successful, Healthy, Enabled; completed SH query returns its events. |
| V07 | End-to-end visibility | **PASS**: 129,310 existing events in the recorded 24-hour query; three expected sourcetypes. |
| V08 | Metrics fields and dashboard | **PASS within sample**: six of six events have CPU/RAM fields; dashboard rendered 5.4% / 21.02%. No broad timestamp or measurement-accuracy audit. |
| V09 | Transport protection | **GAPS OBSERVED**: Web uses HTTP; forwarding receiver is plain `splunktcp`; peer URI uses HTTPS but certificate verification was not established. |
| V10 | Preservation | **CONFIGURATION VERIFIED**: 41 private source files verified, 19 reviewed artifacts published. Event-export and independent-backup status are tracked separately. |

## Distributed search observation

[Query](../searches/validate-data-path.spl), executed through SH. Search interval: **2026-11-02 16:26:28 UTC to 2026-11-03 16:26:28 UTC**. Splunk displayed completion and 129,310 matched events.

| host | sourcetype | splunk_server | count | Latest event UTC |
| --- | --- | --- | ---: | --- |
| splunk-uf | linux_boot | splunk-idx | 52,045 | 2026-11-02 23:09:10 |
| splunk-uf | linux_messages | splunk-idx | 77,242 | 2026-11-03 16:26:27 |
| splunk-uf | system_metrics | splunk-idx | 23 | 2026-11-03 16:25:01 |

These are historical counts, not an expectation that every source produces new events every minute. [Screenshot](../evidence/screenshots/splunk-distributed-search.jpg).

## Parsing and dashboard observation

[Field query](../searches/validate-metric-fields.spl), interval **2026-11-03 15:59:16 to 16:29:16 UTC**: count=6, cpu_parsed=6, ram_parsed=6. Latest event=16:25:01 UTC, CPU=5.40, RAM=21.02, host=`splunk-uf`, peer=`splunk-idx`. [Screenshot](../evidence/screenshots/splunk-field-validation.jpg).

The [reviewed source excerpt](../evidence/validation/metrics-sample.txt) contains only timestamps and percentages. The [dashboard screenshot](../evidence/screenshots/splunk-dashboard.jpg) showed matching values at capture. Its hardcoded `earliest=-5m` and five-minute sample cadence limit the meaning of an average; see [lessons learned](lessons-learned.md).

## Runtime evidence

Selected, sanitized diagnostics: [SH](../evidence/validation/splunk-sh-diagnostics.txt), [IDX](../evidence/validation/splunk-idx-diagnostics.txt), [UF](../evidence/validation/splunk-uf-diagnostics.txt). Full diagnostic captures remain private. `btool` describes merged on-disk configuration; listeners, sockets and successful searches supply separate runtime evidence.

Search-peer health was positive, while the **Search Head's local health** was yellow for disk space and I/O wait. DiskMon reported 9,532 MB remaining below twice its 5,000 MB minimum; the IOWait panel reported a yellow threshold of 1. These warnings were observed, not repaired. The healthy peer label does not mean the whole deployment was free of warnings.

`splunk_server` identifies the peer associated with results; [official guidance](https://help.splunk.com/en/splunk-enterprise/search/search-manual/10.2/retrieve-events/search-across-one-or-more-distributed-search-peers). It does not establish loss-free ingestion, redundancy or restore success.

## Interview-readiness check — 2026-11-06

A later live query for the last 20 minutes was refused because the Search Head dispatch directory reached the configured minimum free space. The backup operation left a verified 1.3 GB archive on that host; service state was still active/running. This check does not supersede the historical passing results above, but the current lab must not be described as ready for a live demonstration until storage is released and a fresh query succeeds.
