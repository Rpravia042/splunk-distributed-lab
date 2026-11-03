# Security and sensitive data

## Preservation rules

The owner requires explicit approval before any Google Cloud resource modification or deletion. Starting a stopped VM, changing firewall/IAM/metadata, adding SSH access, snapshots, disk attachment and shutdown are outside the current read-only inspection. Guest services may start automatically at boot.

Private repository visibility is not a substitute for sanitization. Never commit credentials, tokens, private keys, Splunk's `splunk.secret`, password databases, license files, authentication bundles, raw logs, cloud credential exports or original assessment material. Encrypted Splunk values are still sensitive.

## Review pipeline

1. Collect only relevant configuration into `.recovery/` on the local computer. Restrict directory permissions. Do not upload raw captures to GitHub.
2. Record capture provenance and incomplete or denied reads locally.
3. Use `scripts/sanitize.py` to make a separate candidate copy. Supply known project IDs, account names, live hostnames/addresses and sensitive script arguments through a private literal-replacement map.
4. Review every candidate manually. Automated patterns cannot recognize all custom credentials, personal data, command arguments, dashboard text or business context.
5. Review filenames and screenshots too. Prefer cropping at capture time; do not cover text with translucent shapes or retain recoverable layers. The included JPEG crops were captured directly from the console and visually reviewed.
6. Promote only reviewed candidates to `configs/recovered/` or `evidence/`, update the evidence register and run repository checks.
7. Before public release, review the complete Git history and remote contents, not just the working tree. Do not upload an archive of the working directory.

The scripts do not guarantee that a file is safe to publish. `check_repo.py` reports recognizable problems without printing matching sensitive values. It is a repository check, not a comprehensive security scanner or a cloud validation.

## If a secret is discovered

Keep it out of commits and reports. Identify the credential type and affected system without repeating its value. Coordinate revocation/rotation with the owner before changing the lab. Deleting a secret from the latest file alone does not remove it from Git history. No credential rotation has been performed by this project.
