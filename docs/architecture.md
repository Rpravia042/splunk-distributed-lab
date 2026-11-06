# Architecture

## Observed data path

1. On `splunk-uf`, a cron job runs `/usr/local/bin/system_metrics.sh` every five minutes. It appends timestamp, CPU usage and RAM usage to `/var/log/splunk-lab/system_performance.log`.
2. Universal Forwarder monitors that file plus `/var/log/messages` and `/var/log/boot.log`, assigning index `linux_os` and sourcetypes `system_metrics`, `linux_messages` and `linux_boot`.
3. UF forwards to the indexer's TCP 9997 receiver. Both hosts showed the same established connection during inspection.
4. `splunk-idx` stores the events under `$SPLUNK_DB/linux_os/{db,colddb,thaweddb}`.
5. `splunk-sh` uses an HTTPS search-peer URI on TCP 8089. The peer UI and completed queries confirm distributed search.
6. The analyst opens Splunk Web on the Search Head, TCP 8000, and views the recovered dashboard.

## Network flows and evidence

| Source | Destination | Port | Observed evidence |
| --- | --- | --- | --- |
| UF | IDX | TCP 9997 | Recovered outputs/receiver, effective configuration, active socket, indexed events |
| SH | IDX | TCP 8089 | Recovered and effective `distsearch.conf`, healthy peer, search results |
| Administrator | SH | TCP 8000 | Authenticated Splunk Web session; HTTP and `enableSplunkWebSSL=false` |
| Administrator | Linux nodes | TCP 22 | Owner-authorized browser SSH with temporary access |

The indexer also had TCP 8000 and 8089 listeners. The UF had no listening socket on 8000, 8089 or 9997 at capture. Listener presence and VPC rules alone do not establish Internet reachability. See [network review](network-review.md).

## Boundaries

All VMs share one zone and the default VPC. One indexer is a single failure domain; no indexer cluster, SH cluster, cluster manager or replication guarantee was demonstrated. The forwarding receiver uses `splunktcp`, not a TLS receiver, and UF effective `useACK=false`. Search-peer HTTPS does not itself prove certificate identity verification. These are preserved lab limitations, not recommended production settings.

Conventional component relationships are documented in [Splunk's network guide](https://help.splunk.com/?resourceId=Splunk_InheritedDeployment_Ports). The [rebuild guide](rebuild.md) separates future security choices from recovered behavior.
