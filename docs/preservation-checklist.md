# Before retiring Google Cloud

**Status: NOT READY FOR DELETION. No deletion has been authorized or performed.**

- [x] Inventory the three VMs, source images, disks and visible VPC rules.
- [x] Obtain explicit boot and temporary SSH authorization; validate running state.
- [x] Recover and hash-check 41 original configuration/service/script/metadata/source files.
- [x] Inspect common custom-script paths, services and cron; document collection boundaries.
- [x] Publish 19 reviewed artifacts with provenance and reasons for 22 private-only omissions.
- [x] Validate services, forwarding, index routing, distributed search, metric fields and dashboard.
- [x] Capture real evidence and review images for sensitive information.
- [x] Confirm the owner wants all original indexed events preserved privately.
- [x] Generate and fully verify the current server-side export: 8,697,141 events across six populated event indexes.
- [ ] Complete download and verify the local archive against the server SHA-256.
- [ ] Verify an independent private backup, including the event export; test reconstruction in a separate environment.
- [ ] Finish review of remaining instance metadata, guest firewall, other snapshot types and effective IAM if a full infrastructure reconstruction is required.
- [x] Review published contents and history; verify subsequent changes before publication. The audit through commit `e08d955` covered 86 unique text blobs and seven reviewed images with no recognizable sensitive findings.
- [ ] Verify checks for any subsequent changes before public release.
- [ ] Obtain explicit authorization for the exact shutdown or deletion action.

The original census at **2026-11-03 16:35:30 UTC** found 666,094 events. The received JSON was truncated after 13,371 complete records and was rejected. The expanded capture at **2026-11-06 22:38:22 UTC** contains **8,697,141 events**. Its server-side compressed CSV passed complete parsing, count, field and gzip checks. A verified local download is still required. See the [event backup guide](event-backup.md).

**Current operational issue:** retaining the archive on the 20 GB Search Head left about 5.05 GB free. A live query on 2026-11-06 was refused because Splunk's 5,000 MB minimum for the dispatch directory was reached. The service remained active. Downloading and verifying the archive, then releasing its server-side storage, is required before declaring the lab ready for an interview demonstration. No configuration, disk size or retention setting has been changed to work around this.

A working-tree copy or a single local archive is not an independent backup. Configurations and event JSON are not a byte-for-byte disk or Splunk bucket backup. Restore success remains untested. A completed checklist is not itself authorization to delete. No teardown script is included.
