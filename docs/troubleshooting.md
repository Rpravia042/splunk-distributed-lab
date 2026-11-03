# Troubleshooting

These are diagnostic paths, not claims about incidents that occurred in the original lab. Diagnose first and record evidence before proposing a change.

| Symptom | Inspect first | How to interpret it |
| --- | --- | --- |
| SSH unavailable | Compute Engine power state and existing access method | All three VMs were stopped at inspection; opening ports will not fix that state |
| UF has no outgoing data | Source permissions, effective `inputs.conf`, file growth, `outputs.conf` | Confirm a source exists and targets the intended index before blaming networking |
| UF cannot reach IDX | Destination resolution, receiver listener, guest firewall and VPC rules | An allow rule is not proof of a listener; inspect broad inherited/default rules too |
| Events arrive in an unexpected index | Input stanza, transforms and destination index existence | Read merged settings with source attribution; a local file can be overridden |
| Search returns no events | Time range/timezone, index, role permissions, peer status | Empty results do not distinguish missing data from a search scope problem |
| SH cannot search IDX | Management listener, peer URI, trust/authentication and certificate validation | TCP 8089 reachability alone does not prove authenticated distributed search |
| Timestamps or fields are wrong | Raw event privately, sourcetype, `props.conf` and transforms | Compare event time with ingestion time; do not publish original sensitive events |
| Indexer stops accepting data | Free space, index paths, permissions and service logs | Capture failure evidence; do not delete buckets or reset indexes |
| Settings appear ignored | `btool <name> list --debug`, service start/reload history | Effective on-disk configuration may differ from loaded configuration |

Do not restart services, disable TLS, broaden firewall access, rotate credentials or rewrite configuration as part of evidence collection. Propose a specific correction separately if needed. Keep passwords out of command arguments and screenshots.
