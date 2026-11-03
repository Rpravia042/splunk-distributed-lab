# Evidence register

Capture date: **2026-11-03**. Source: authenticated Google Cloud console. Infrastructure observation was read-only. The original application files have not been collected.

| ID | Artifact | Provenance | What it proves | What it does not prove |
| --- | --- | --- | --- | --- |
| E01 | [VM state crop](screenshots/gcp-instances-stopped.jpg) | Direct console screenshot, cropped at capture | Three VM names, zone and stopped icons | Installed Splunk roles, services or ingestion |
| E02 | [Infrastructure](../docs/infrastructure.md) | Sanitized transcription of each VM detail page | Machine type, source image, disk settings and visible security settings | Guest package state, backups or restore success |
| E03 | [Firewall crop](screenshots/gcp-firewall-rules.jpg) and [review](../docs/network-review.md) | Direct console crop and sanitized table transcription | Visible VPC rules and their displayed attributes | Effective inherited policy, guest firewall or Internet reachability |
| E04 | Guest configuration | Not yet collected | — | Recovery remains incomplete |
| E05 | End-to-end search screenshot | Not yet captured | — | No live success claim |
| E06 | [Snapshot inventory](../docs/infrastructure.md) | Sanitized transcription of standard-snapshot list | One available scheduled SH-disk snapshot; none listed for IDX/UF | Contents, other snapshot categories, restore success or complete lab backup |

Screenshots are genuine console crops, not mockups. Cropping excluded account, organization, project and address details. Source filter values are not expanded in the firewall capture; use the transcription and its limitations. No blurring or generative editing was used.

`SHA256SUMS` covers the included screenshots. Review the images visually as well as checking hashes. Repository test results are documented under [validation](validation/repository-checks.md) and do not establish that Splunk works.
