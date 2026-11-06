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
- [ ] Complete and verify private export of the six observed populated event indexes.
- [ ] Verify an independent private backup, including the event export; test reconstruction in a separate environment.
- [ ] Finish review of remaining instance metadata, guest firewall, other snapshot types and effective IAM if a full infrastructure reconstruction is required.
- [ ] Verify final GitHub files/checks and review history before public release.
- [ ] Obtain explicit authorization for the exact shutdown or deletion action.

The event census at **2026-11-03 16:35:30 UTC** found 666,094 events across six populated indexes. A prepared JSON export covers existing events from epoch zero to that exclusive cutoff through the current administrative search permissions. Chrome blocked the initial download. The file supplied on 2026-11-06 contains 13,371 complete records and ends in truncated JSON; it fails the expected 666,094-event census. A complete event export remains outstanding. See the [event backup guide](event-backup.md). Events generated after the cutoff are outside this capture.

A working-tree copy or a single local archive is not an independent backup. Configurations and event JSON are not a byte-for-byte disk or Splunk bucket backup. Restore success remains untested. A completed checklist is not itself authorization to delete. No teardown script is included.
