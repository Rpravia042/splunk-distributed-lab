# Configuration provenance

`recovered/` contains **reviewed derivatives of original files** read from the three VMs. Its [manifest](recovered/manifest.json) records original paths, capture times, published SHA-256 hashes, redactions and private-only omissions. It covers 41 recovered source files; 19 selected artifacts are published, including the original script and cron schedule.

Original source paths under `etc/` are relative to `/opt/splunk` or `/opt/splunkforwarder`, except `etc/systemd/`, which is relative to the filesystem root. The manifest makes this explicit. The original `/usr/local/bin/system_metrics.sh` is in [scripts/original](../scripts/original/system_metrics.sh).

`examples/` contains newly authored minimal snippets using the illustrative index `lab`. They are **not the original configuration**; the observed index was `linux_os`. Example input/receiver stanzas are disabled intentionally. Neither directory is a complete secure deployment.

Do not install redacted `server.conf` or copied service units verbatim. Generate new credentials, host identity, certificates and service configuration for a rebuild. `indexer.example.invalid` replaces a live private address and will not resolve as a real destination.
