# Troubleshooting

The table gives diagnostic paths. Observed recovery issues are recorded separately below; suggested fixes have not been applied to the original lab.

| Symptom | Inspect first | How to interpret it |
| --- | --- | --- |
| SSH unavailable | Compute Engine power state and existing access method | The VMs were initially stopped; after authorized boot, browser SSH sessions sometimes failed or disconnected. Reopening an authorized session allowed recovery |
| UF has no outgoing data | Source permissions, effective `inputs.conf`, file growth, `outputs.conf` | Confirm a source exists and targets the intended index before blaming networking |
| UF cannot reach IDX | Destination resolution, receiver listener, guest firewall and VPC rules | An allow rule is not proof of a listener; inspect broad inherited/default rules too |
| Events arrive in an unexpected index | Input stanza, transforms and destination index existence | Read merged settings with source attribution; a local file can be overridden |
| Search returns no events | Time range/timezone, index, role permissions, peer status | Empty results do not distinguish missing data from a search scope problem |
| SH cannot search IDX | Management listener, peer URI, trust/authentication and certificate validation | TCP 8089 reachability alone does not prove authenticated distributed search |
| Timestamps or fields are wrong | Raw event privately, sourcetype, `props.conf` and transforms | Compare event time with ingestion time; do not publish original sensitive events |
| Indexer stops accepting data | Free space, index paths, permissions and service logs | Capture failure evidence; do not delete buckets or reset indexes |
| Settings appear ignored | `btool <name> list --debug`, service start/reload history | Effective on-disk configuration may differ from loaded configuration |

Do not restart services, disable TLS, broaden firewall access, rotate credentials or rewrite configuration as part of evidence collection. Propose a specific correction separately if needed. Keep passwords out of command arguments and screenshots.

## Issues observed during recovery

- **Intermittent SSH and failed browser downloads:** new browser SSH sessions allowed file reads; small hashed transfers recovered configuration. No network policy or SSH server settings were changed.
- **Cloud telemetry permission failures:** SH serial output contained Ops Agent errors for `logging.logEntries.create` and `monitoring.timeSeries.create`. They concern Cloud Logging/Monitoring and do not by themselves explain SSH failures or Splunk ingestion. Full logs remain private; no IAM change was made.
- **Splunk Web event download blocked:** Chrome returned `ERR_BLOCKED_BY_CLIENT` for the export. A manual owner download was requested; export is not considered complete until the local file passes count and readability checks.
- **Disk and I/O warnings:** SH local health showed yellow disk-space and IOWait warnings despite completed searches. Diagnose growth, retention and workload before increasing capacity or changing thresholds.
- **Dashboard time-range mismatch:** compare the hardcoded five-minute SPL filter with global and data-source time parameters. Preserve the original while testing a corrected version in a separate environment.
