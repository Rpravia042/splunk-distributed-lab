# Splunk Distributed Lab

A working three-node Splunk lab on Google Cloud: Linux logs and scheduled CPU/RAM samples travel through a Universal Forwarder to an Indexer, then become searchable from a separate Search Head.

**Recovered on 3 November; live searches revalidated on 7 November 2026.** The original configuration, metrics script, schedule and Dashboard Studio definition are preserved with provenance. The original three VMs are retained for future demonstrations. After a private event backup exhausted the Search Head's search-space reserve, an owner-authorized disk and XFS expansion restored searches. A fresh query returned recent UF samples from the Indexer, and the original dashboard rendered CPU/RAM values. [Current status and preservation limits](docs/preservation-checklist.md).

## Personal monitoring pilot

[Installable monitoring apps and verification steps](personal-lab/README.md) for a separate three-node rebuild. The pilot adds filesystem capacity, missing-source detection and ingestion delay. Live validation of the personal environment is pending.

## Architecture

![Validated Splunk lab topology](docs/architecture.svg)

[Editable Mermaid source](docs/architecture.mmd) · [Architecture details](docs/architecture.md)

| Node | Responsibility | Observed environment |
| --- | --- | --- |
| `splunk-uf` | Monitor three Linux sources and forward to TCP 9997 | Universal Forwarder; `splunkfwd` service account |
| `splunk-idx` | Receive events, maintain `linux_os`, answer searches | Splunk Enterprise; `splunk` service account |
| `splunk-sh` | Splunk Web, distributed search and dashboard | Splunk Enterprise; `splunk` service account |

All three run Splunk 10.6.1.1 (build `b2ae2962645c`) on CentOS Stream 10, using `e2-medium` VMs with 2 vCPU and 4 GB RAM in `us-central1-c`. All originally had 20 GB balanced disks; SH now has 30 GB after the authorized capacity repair. IDX and UF retain 20 GB disks. Vendor compatibility and production sizing are not established. It is a single-indexer deployment without high availability.

## Demonstrated results

- All three Splunk services were running after the owner-authorized boot.
- UF-to-IDX forwarding had an established TCP connection; the indexer listened on 9997.
- A Search Head query returned **129,310 events** over its recorded 24-hour interval, across `linux_boot`, `linux_messages` and `system_metrics`, with `splunk_server=splunk-idx`.
- The search peer was **Up / Successful / Healthy / Enabled**.
- A separate 30-minute query found six metric events, with CPU and RAM fields extracted in all six. The original dashboard displayed CPU **5.4%** and RAM **21.02%** at capture time.

![Distributed search with three source types and the expected indexer](evidence/screenshots/splunk-distributed-search.jpg)

These are observations at specific capture times, not throughput, durability or availability guarantees. The Search Head also reported yellow disk-space and I/O-wait warnings. [Validation details and limitations](docs/validation.md).

On **7 November 2026**, a completed 20-minute query found four metric events from `splunk-uf` on `splunk-idx`, latest **14:45:02 UTC**. SH had about **15.0 GB free** after the repair. The private archive contains **8,697,141 events** through its fixed cutoff; its local copy matches the fully validated server archive by size and SHA-256. No full restore has been tested.

![Successful search after the capacity repair](evidence/screenshots/splunk-search-restored.png)

## Original dashboard

![Original UF System Performance dashboard](evidence/screenshots/splunk-dashboard.jpg)

The screenshot and XML preserve the original panel title, including its typo, and the original time-range behavior. [Dashboard review](docs/lessons-learned.md) explains improvements for a separate rebuild.

## Explore the project

| Topic | Material |
| --- | --- |
| Recovered source and provenance | [Configuration guide](configs/README.md), [manifest](configs/recovered/manifest.json) |
| Original data generator | [system_metrics.sh](scripts/original/system_metrics.sh), [five-minute cron schedule](configs/recovered/universal-forwarder/splunkfwd.crontab) |
| Rebuild in a separate environment | [Rebuild guide](docs/rebuild.md) |
| Infrastructure and access | [Inventory](docs/infrastructure.md), [network review](docs/network-review.md) |
| Evidence and validation | [Evidence register](evidence/README.md), [validation](docs/validation.md), [SPL queries](searches) |
| Recovery and security | [Recovery runbook](docs/recovery.md), [private event backup](docs/event-backup.md), [security](SECURITY.md) |
| Troubleshooting and lessons | [Troubleshooting](docs/troubleshooting.md), [lessons learned](docs/lessons-learned.md) |
| Español | [Guía breve](docs/guia-es.md) |

## Repository checks

Python 3.9+; no external Python dependencies:

```sh
python3 -m unittest discover -s tests -v
python3 scripts/check_repo.py
bash -n scripts/original/system_metrics.sh
```

Checks cover collection boundaries, sanitization, artifact integrity and dashboard syntax. They do not replace live Splunk validation or manual sensitive-data review.

## Scope and attribution

A personal portfolio project originally built for a technical assessment. It contains no assessment prompt, employer material, customer records, Splunk binaries or license files, and is not an official vendor or employer deployment. Raw recovery bundles, credentials and event exports remain outside GitHub. Published configurations are reviewed derivatives, not a production deployment package.
