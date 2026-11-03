# Lessons learned

## Supported by this inspection

1. **Preserve before teardown.** All three boot disks are configured to be deleted with their VMs. A professional handoff requires recovered configuration and a verified backup before retirement.
2. **Inventory is not application validation.** The console confirms machine properties and power states. It cannot establish forwarding success, installed versions or search correctness.
3. **Targeted firewall rules do not imply isolation.** The lab has role-specific Splunk rules, alongside broad default internal and administrative rules. Review the whole policy set; inherited policies could not be inspected with the current permissions.
4. **Snapshot schedules need evidence.** A visible schedule does not prove a completed snapshot or a successful restore.
5. **Recovery needs provenance.** Original files, sanitized derivatives and new reference examples must be clearly labeled so a reviewer can judge the evidence.

## Improvements for a future deployment

Use a dedicated VPC and scoped administration; verify TLS and host identity; document supported OS/version combinations; size the indexer for measured ingestion and retention; preserve reproducible configuration; test restore procedures. These improvements have not been applied to the original lab.

## Owner retrospective still to capture

The original setup sequence, assessment constraints, actual failures and fixes, design tradeoffs and live results remain to be recovered from files and the owner's experience. Do not invent a successful incident-resolution story or performance metrics to fill these gaps.
