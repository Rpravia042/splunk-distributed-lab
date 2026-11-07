# Troubleshooting

The table gives diagnostic paths. Observed recovery issues and the owner-authorized capacity repair are recorded separately below.

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
- **Splunk Web event download blocked:** Chrome returned `ERR_BLOCKED_BY_CLIENT`; the supplied JSON was truncated. A later compressed server export passed full parsing, and its completed private SSH transfer matched the server byte count and SHA-256. The temporary backup key was removed after transfer.
- **Disk and I/O warnings:** SH local health showed yellow disk-space and IOWait warnings despite completed searches. Diagnose growth, retention and workload before increasing capacity or changing thresholds.
- **Dashboard time-range mismatch:** compare the hardcoded five-minute SPL filter with global and data-source time parameters. Preserve the original while testing a corrected version in a separate environment.

## Backup storage incident — 2026-11-06

The combined event export generated a 1,315,156,954-byte compressed archive and used additional search-job storage. The export was finalized when free space fell below the planned margin. Its six index counts matched the census, and a subsequent complete CSV/gzip check passed for all 8,697,141 events.

The retained archive still reduced Search Head free space to roughly 5.05 GB. A new search was then refused with the dispatch minimum-free-space check of 5,000 MB. `Splunkd.service` remained active. The distributed-search configuration, server configuration, dashboard XML, service unit and version file matched their original recovered SHA-256 hashes.

**Resolved on 2026-11-07:** the local archive was verified, and the owner chose to keep the server copy too. The owner authorized increasing only SH's existing boot disk from 20 to 30 GB. The console resize did not automatically grow this guest's root partition. Read-only checks established `/dev/sda2` as the XFS root, a 30 GB `/dev/sda`, and contiguous free space after partition 2. The repair adjusted GPT to the device size, extended partition 2 to the disk end and ran `xfs_growfs -d /`. No formatting, partition start change, EFI change, reboot or Splunk restart was needed. [Google's disk-resize guidance](https://docs.cloud.google.com/compute/docs/disks/resize-persistent-disk) describes separate partition and filesystem growth when required.

The final check showed about 15.0 GB free and the original SH service still active. A fresh completed query found four recent metric events from UF on IDX, and the original dashboard rendered CPU 4% / RAM 23.23%. Five key SH configuration/service/version files matched their original hashes. The server archive remained present at its verified size. No buckets, index data or archive were deleted; the 5,000 MB minimum was unchanged. See [validation](validation.md) and the [change record](change-record.md).

This incident demonstrates that archive size, intermediate search artifacts and operational free-space reserves must be budgeted separately. Successful searches resolve this blocking symptom; they do not establish that every historical health warning or long-term capacity concern is resolved.
