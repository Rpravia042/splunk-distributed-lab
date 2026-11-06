# Lessons learned

## Findings supported by recovered evidence

1. **Prove each stage separately.** Configuration showed intent; source-read checks, matching sockets, indexer results and the SH query demonstrated the actual path. Neither a firewall rule nor an active service alone proved ingestion.
2. **Make index naming consistent.** The actual index is `linux_os`; generic examples use `lab`. Mixing them during a rebuild would produce misleading empty searches.
3. **Time controls need one clear meaning.** The dashboard displays a global 24-hour picker but its SPL includes `earliest=-5m`, alongside data-source time parameters. A future dashboard should use one documented time source. The original title also omits the initial “A” in “Average”; it is preserved as evidence.
4. **Sampling cadence affects interpretation.** The generator runs every five minutes. A five-minute average can contain only one sample or temporarily none. Show sample count and last-event age, and choose a window aligned with the cadence.
5. **A working lab can still have resource warnings.** SH local health reported yellow disk-space and I/O-wait states. Successful searches and a Healthy peer did not establish production capacity. Measure ingestion, disk growth and query load before sizing a rebuild.
6. **Narrow rules can coexist with broad access.** Role-specific Splunk rules exist alongside broad default internal/SSH/RDP rules. Inherited policy visibility was incomplete. Review the full effective policy before claiming isolation.
7. **Encryption must be checked by path.** Web HTTP, a plain TCP forwarding receiver and an HTTPS peer URI have different protection properties. Credentials and encrypted password values still needed removal from recovered configuration.
8. **Sanitization must preserve meaning and syntax.** A four-part product version resembles an IPv4 address; a Dashboard Studio `token` can be a UI variable. Review context, preserve JSON/XML syntax and retain a private original with hashes.
9. **Recovery needs usable exports and provenance.** Browser SSH sessions were intermittent and its file-download workflow failed. Bounded, hashed configuration transfers recovered the useful files; raw copies and sanitized derivatives remain separate.
10. **A schedule is not a tested backup.** One SH snapshot was visible, while no standard snapshots for IDX/UF appeared. All boot disks delete with their VMs. Independent backup verification is required before retirement.

## Improvements for a new deployment

Use a dedicated VPC, scoped administration, verified TLS, supported OS/version combinations, reproducible app configuration, log rotation, deliberate retention and a tested restore procedure. Review UF acknowledgement requirements and the single-indexer failure domain. None of these changes were applied to the original running lab.

The owner's original assessment constraints and setup history are not reconstructed from assumptions. This document records inspected behavior and future improvements, not invented incidents or performance achievements.
