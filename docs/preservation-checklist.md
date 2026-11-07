# Preservation and demonstration status

**Current plan: retain the same three VMs for an interview. Searches and the original dashboard passed fresh checks on 2026-11-07. No deletion has been authorized or performed.** This checklist also records what would remain necessary if cloud retirement is requested later.

- [x] Inventory the three VMs, source images, disks and visible VPC rules.
- [x] Obtain explicit boot and temporary SSH authorization; validate running state.
- [x] Recover and hash-check 41 original configuration/service/script/metadata/source files.
- [x] Inspect common custom-script paths, services and cron; document collection boundaries.
- [x] Publish 19 reviewed artifacts with provenance and reasons for 22 private-only omissions.
- [x] Validate services, forwarding, index routing, distributed search, metric fields and dashboard.
- [x] Capture real evidence and review images for sensitive information.
- [x] Confirm the owner wants all original indexed events preserved privately.
- [x] Generate and fully verify the current server-side export: 8,697,141 events across six populated event indexes.
- [x] Complete download and verify the local archive against the server byte count and SHA-256.
- [x] Retain both server and local event archives, as requested by the owner.
- [x] Complete the authorized SH 20→30 GB disk/partition/XFS expansion; repeat a small search and render the original dashboard.
- [ ] Keep an additional private copy off this computer and test reconstruction in a separate environment before any eventual retirement.
- [ ] Finish review of remaining instance metadata, guest firewall, other snapshot types and effective IAM if a full infrastructure reconstruction is required.
- [x] Review published contents and history; verify subsequent changes before publication. The audit through commit `e08d955` covered 86 unique text blobs and seven reviewed images with no recognizable sensitive findings.
- [x] Review subsequent published changes; run repository checks and verify remote file hashes before completing each publication.
- [ ] Obtain explicit authorization for the exact shutdown or deletion action.

The original census at **2026-11-03 16:35:30 UTC** found 666,094 events. The received JSON was truncated after 13,371 complete records and was rejected. The expanded capture at **2026-11-06 22:38:22 UTC** contains **8,697,141 events**. Its server-side compressed CSV passed complete parsing, count, field and gzip checks. The completed local copy matches its **1,315,156,954 bytes** and SHA-256. The backup-only temporary key was removed after transfer. See the [event backup guide](event-backup.md).

**Capacity incident resolved:** the retained export and temporary search storage exhausted SH's free-space reserve. The owner explicitly chose to keep the server archive and authorized expanding the existing SH disk to 30 GB. Guest GPT, root partition and XFS growth completed on 7 November. About 15.0 GB was available at the final check; a new query returned four recent UF metric events from IDX, and the original dashboard rendered values. The service was not restarted, and five key SH files matched their recovered hashes. No retention setting, search-space threshold, IDX/UF disk or Splunk configuration was changed. [Detailed changes](change-record.md).

The private local event archive is separate from Google Cloud, but an additional off-computer copy is still advisable before retirement. Configurations and event exports are not a byte-for-byte disk or Splunk bucket backup. Restore success remains untested. A completed checklist is not itself authorization to delete. No teardown script is included.
