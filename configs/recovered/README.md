# Recovered original material

Captured from authorized SSH sessions on 2026-11-03. Files retain their original stanzas and values except documented redactions. Full raw copies and their original hashes are stored privately outside GitHub.

| Role | Published material |
| --- | --- |
| Search Head | Distributed search, sanitized server settings, version, systemd unit, Dashboard Studio XML and dashboard metadata |
| Indexer | `linux_os` index, TCP 9997 receiver, sanitized server settings, version, systemd unit and search-app metadata |
| Universal Forwarder | Three monitored sources, forwarding destination, sanitized server settings, version, systemd unit and cron schedule |
| Data generator | [Original CPU/RAM script](../../scripts/original/system_metrics.sh) |

See [manifest.json](manifest.json) for every published artifact and each private-only file. Generated route definitions, telemetry identifiers, learned heuristics, UI preferences and unrelated generated metadata were recovered privately but omitted from the portfolio. Authentication stores, licenses, private keys and Splunk binaries were intentionally outside the collection scope.

The dashboard's `global_time` token is a UI variable, not an authentication credential. It remains intact. The XML and its embedded JSON are validated during repository checks. No dashboard or service configuration was changed on the running lab.
