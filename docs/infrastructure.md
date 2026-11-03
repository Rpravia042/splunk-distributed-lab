# Infrastructure inventory

Inspected in the authenticated Google Cloud console on **2026-11-03**, using read-only views. This is a sanitized transcription, not a raw API export.

| Property | splunk-sh | splunk-idx | splunk-uf |
| --- | --- | --- | --- |
| State | Stopped | Stopped | Stopped |
| Zone | us-central1-c | us-central1-c | us-central1-c |
| Machine | e2-medium | e2-medium | e2-medium |
| vCPU / memory | 2 / 4 GB | 2 / 4 GB | 2 / 4 GB |
| Image | centos-stream-10-v20261024 | centos-stream-10-v20261024 | centos-stream-10-v20261024 |
| Architecture | x86_64 | x86_64 | x86_64 |
| VPC / subnet | default / default | default / default | default / default |
| NIC | nic0 | nic0 | nic0 |
| Network tag | splunk-sh | splunk-idx | splunk-uf |
| Boot disk | 20 GB pd-balanced | 20 GB pd-balanced | 20 GB pd-balanced |
| Disk deletion behavior | Delete with VM | Delete with VM | Delete with VM |
| VM deletion protection | Disabled | Disabled | Disabled |
| Snapshot schedule shown | default-schedule-1 | default-schedule-1 | default-schedule-1 |
| Secure Boot | Disabled | Disabled | Disabled |
| vTPM / integrity monitoring | Enabled / enabled | Enabled / enabled | Enabled / enabled |

The source image identifies the initial OS image; packages and OS changes inside the disks have not been inspected. The external-address column was empty while the VMs were stopped. This does not establish their exposure while running.

The console showed a daily snapshot schedule beginning between 17:00 and 18:00 in its displayed timezone. A schedule is **not evidence of a complete or restorable backup**.

The standard-snapshot list contained one available scheduled snapshot, associated with the Search Head's original boot disk. It was created on **2026-11-02 at 11:38:31 UTC-06:00**, showed 1.24 GB snapshot size and a 20 GB source disk. No standard snapshots for the Indexer or Universal Forwarder appeared in that list. Archive, instant and recycled snapshots were not inspected. Snapshot contents and restore success remain unverified; this is not a backup of the complete distributed lab.

## Missing inventory

See the separately captured [network review](network-review.md) for the seven visible VPC firewall rules and the limitation on inherited-policy visibility.

- Installed Splunk/UF version, build, service user and installation path.
- Guest firewall, listening sockets, disk utilization and startup behavior.
- Effective Splunk configuration, custom apps, dashboards, saved searches and scripts.
- Project-level metadata/startup scripts, other snapshot categories, effective IAM, routes and hierarchical firewall policies.
- Configuration and data recovery from guest disks.

Do not delete VMs or the project while these preservation tasks remain open.
