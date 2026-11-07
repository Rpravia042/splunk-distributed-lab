# Recovery and capacity change record

The same three VMs are retained for a future interview. This record distinguishes recovery activity from changes to the original application.

| Activity | Authorization and result |
| --- | --- |
| Power-on and browser SSH | Explicit owner approval for the three named VMs. Existing services started automatically. Browser SSH uses temporary access. |
| Configuration recovery | Relevant files were read and copied privately; reviewed derivatives were published. Original Splunk configuration was not rewritten. |
| Event preservation | Owner requested all indexed events accessible to the search account. The fixed-cutoff export contains 8,697,141 events; complete server parsing passed. The local archive matches server size and SHA-256. |
| Backup transfer access | Separate approval for a 15-minute, forced-command key limited to reading the archive, without a shell or forwarding. The exact entry was removed after transfer; the local private key was deleted. |
| Archive retention | Owner explicitly chose to retain the server archive. It remains on SH as well as privately on the local computer. |
| SH capacity | Explicit approval to expand only the existing SH boot disk from 20 to 30 GB and adjust partition/filesystem if needed. Adds 10 GB of billable storage; no direct in-place disk shrink. |
| Guest capacity repair, 7 November | Disk was 30 GB but root partition remained about 20 GB. Adjusted GPT, extended the end of partition 2 and grew its XFS filesystem online. Root start sector and EFI partition preserved. No reboot or Splunk restart. |

## Verification after the repair

- At **2026-11-07 14:47:53 UTC**, root filesystem total was 31,934,361,600 bytes, with 15,011,602,432 bytes available.
- SH `Splunkd.service` remained active/running, started **2026-11-03 15:55:57 UTC**.
- Five key SH files matched their original recovered SHA-256 hashes: distributed-search configuration, server configuration, dashboard XML, systemd unit and version file.
- The retained server archive remained present at 1,315,156,954 bytes. Its separately verified local copy stays outside GitHub.
- A completed SH search returned four UF metric events from IDX, latest **14:45:02 UTC**; the original dashboard displayed CPU 4% / RAM 23.23%. [Validation and captures](validation.md).

No VM replacement, index deletion, password rotation, firewall/IAM change, Splunk reconfiguration, retention adjustment or weakening of the dispatch-space threshold was performed. IDX and UF disks retain their original sizes. Recovery/search operations did create temporary files and normal job artifacts, and the event archive occupies SH space.

This resolves the observed search-space blocker. It does not claim that all health warnings, transport-security gaps or long-term capacity risks are repaired. No full replay or infrastructure restore has been tested. Shutdown or deletion remains subject to separate owner authorization.
