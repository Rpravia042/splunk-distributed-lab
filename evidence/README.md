# Evidence register

Initial capture date: **2026-11-03**, with post-repair validation on **2026-11-07**. Sources: authenticated Google Cloud console, authorized browser SSH and the owner's authenticated Splunk Web session.

| ID | Artifact | Provenance and meaning | Limits |
| --- | --- | --- | --- |
| E01 | [Stopped VMs](screenshots/gcp-instances-stopped.jpg) | Console crop before owner-authorized boot | Historical initial state |
| E02 | [Running VMs](screenshots/gcp-instances-running.jpg) and [inventory](../docs/infrastructure.md) | Console capture and sanitized transcription | Does not alone prove application health |
| E03 | [Firewall crop](screenshots/gcp-firewall-rules.jpg) and [review](../docs/network-review.md) | Visible VPC rules | Inherited policies and guest firewall not fully inspected |
| E04 | [Recovered artifact manifest](../configs/recovered/manifest.json) | 41 verified original source files; 19 reviewed published artifacts | Selective configuration rescue, not a full disk image |
| E05 | [Distributed search](screenshots/splunk-distributed-search.jpg) | Completed SH query, 129,310 events and three sourcetypes from IDX | Recorded 24-hour interval only |
| E06 | [Peer health](screenshots/splunk-peer-health.jpg) | Up / Successful / Healthy / Enabled | Peer URI cropped out; overall SH health had warnings |
| E07 | [Field validation](screenshots/splunk-field-validation.jpg) | Six events, CPU and RAM extracted in all six | Thirty-minute sample |
| E08 | [Original dashboard](screenshots/splunk-dashboard.jpg) | Rendered original dashboard and metric values | Original typo and time-range mismatch preserved |
| E09 | [SH](validation/splunk-sh-diagnostics.txt), [IDX](validation/splunk-idx-diagnostics.txt), [UF](validation/splunk-uf-diagnostics.txt) | Selected service and effective-configuration excerpts | Full diagnostics retained privately |
| E10 | [Source metric excerpt](validation/metrics-sample.txt) | Three reviewed timestamp/percentage events | No system messages or private event export published |
| E11 | [Snapshot inventory](../docs/infrastructure.md) | One available standard SH-disk snapshot | No verified full-lab restore |
| E12 | [Post-repair search](screenshots/splunk-search-restored.png) | Completed SH query on 7 November, four recent UF samples from IDX | Recorded 20-minute interval only; query inline bounds override the displayed picker |
| E13 | [Post-repair dashboard](screenshots/splunk-dashboard-restored.png) | Original dashboard rendered CPU 4% / RAM 23.23% on 7 November | Original typo and time-range behavior retained |
| E14 | [Capacity repair summary](validation/capacity-repair-20261107.json) | Sanitized console, guest and Splunk observations | Full console/SSH captures remain private; no full restore tested |

Screenshots are direct captures or capture-time crops, not mockups. Account/project/live-address details are excluded. No blurring or generative editing was used. `SHA256SUMS` identifies the visually reviewed images.

The [validation report](../docs/validation.md) records queries, intervals, results and caveats. Repository checks are documented [separately](validation/repository-checks.md). Private event-export progress is tracked in the [preservation checklist](../docs/preservation-checklist.md).
