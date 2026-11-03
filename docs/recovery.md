# Read-only recovery runbook

## Current boundary

All VMs are stopped. No guest collection has run. The owner must authorize power-on and any required temporary SSH-key registration before either action. Do not invoke Cloud Shell, `gcloud compute ssh`, enable APIs or register keys as a workaround for that restriction. An existing connection may be used only within its already authorized access.

## Preparation

Keep a private local recovery directory outside the publication set:

```sh
mkdir -p .recovery
chmod 700 .recovery
```

Before accessing a node, record its state, source image, disk and access path. Avoid restarting services or reloading configuration. Reads and logins can create audit records and update filesystem access times; this workflow avoids intentional configuration changes and is not a forensic disk image.

## File collection after access is available

`scripts/collect_node.py` reads files and streams a tar archive to standard output. It does not run Splunk, install packages, restart services or write an archive on the VM. It selects configuration, dashboards and common script file types under Splunk `etc`, omits authentication/license directories and secret-store files, avoids symlinks, and records unreadable or skipped files. It limits each file to 5 MiB and total included payload to 100 MiB by default.

The example below requires an **already configured and authorized SSH alias**, a verified host key and read permissions for the Splunk files. It does not create cloud access. Output is private and may still contain credentials in ordinary `.conf` files and scripts.

```sh
umask 077
ssh -o BatchMode=yes -o StrictHostKeyChecking=yes splunk-sh \
  'python3 - /opt/splunk' < scripts/collect_node.py > .recovery/splunk-sh.tar
ssh -o BatchMode=yes -o StrictHostKeyChecking=yes splunk-idx \
  'python3 - /opt/splunk' < scripts/collect_node.py > .recovery/splunk-idx.tar
ssh -o BatchMode=yes -o StrictHostKeyChecking=yes splunk-uf \
  'python3 - /opt/splunkforwarder' < scripts/collect_node.py > .recovery/splunk-uf.tar
```

Paths are conventional and must be verified before collection. Missing paths are errors, not empty successful backups. Check SSH exit codes and `collection-report.json` inside each archive. If permissions are insufficient, record the gap and use an authorized existing privileged session; do not change file ownership or permissions. Do not extract unfamiliar archives without reviewing member paths and link types.

## Additional material to inventory

The collector is a bounded first pass, **not a full system backup**. Inspect and recover relevant custom script directories outside Splunk, systemd unit overrides, scheduled tasks, input data generators, app assets with other extensions, project/instance startup metadata and deployment notes. Review individual files before expanding the scope. Do not sweep shell history, home directories, browser profiles, credential stores, index buckets or system logs into the repository.

Record version/build from `etc/splunk.version`, then verify the installation and Linux compatibility against the matching vendor documentation. Review system and app `.conf` files, app/user dashboards, saved searches and role definitions. Redact sensitive fields even when a file otherwise looks like ordinary configuration.

## Effective configuration and validation

After inspecting stored files, use the existing service identity and verified Splunk path to capture selected `btool` outputs into private local evidence. Running Splunk CLI tools may create diagnostic files; do not run them until guest diagnostic execution is authorized. `btool ... --debug` identifies merged settings and source files, but does not prove that the service has loaded current disk changes. See the [Splunk btool guide](https://help.splunk.com/en/splunk-enterprise/administer/troubleshoot/9.3/first-steps/use-btool-to-troubleshoot-configurations).

```text
<SPLUNK_HOME>/bin/splunk btool inputs list --debug
<SPLUNK_HOME>/bin/splunk btool outputs list --debug
<SPLUNK_HOME>/bin/splunk btool indexes list --debug
<SPLUNK_HOME>/bin/splunk btool distsearch list --debug
```

Only run commands relevant to each role. Never place administrator passwords in CLI arguments. Use an authenticated session for read-only status and existing-event searches; do not inject test events without permission. Follow the [validation matrix](validation.md).

## Candidate sanitization and publication

The sanitizer accepts UTF-8 text only and refuses to overwrite a file. A private JSON map contains exact known values as keys and placeholders as values; do not commit the map.

```sh
python3 scripts/sanitize.py .recovery/inputs.conf .recovery/candidates/inputs.conf \
  --map .recovery/redactions.json
```

Inspect the output, add reviewed files individually, update provenance and run local checks. A successful scan is not proof of complete recovery. Verify the remote files and evidence hashes after publication. Keep a separately verified private backup before considering any cloud deletion.
