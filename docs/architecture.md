# Architecture

## Responsibilities

- **splunk-uf:** read configured sources and forward events. Source paths, indexes and sourcetypes await recovery.
- **splunk-idx:** receive and index events, retain buckets, and answer distributed searches.
- **splunk-sh:** provide Splunk Web and dispatch searches to the indexer.

The node roles are owner-reported. Compute Engine independently confirms the three named machines, their zone, source image, machine type and disks. A VM name alone does not verify its Splunk role or running configuration.

## Intended network flows

| Source | Destination | Typical port | Verification needed |
| --- | --- | --- | --- |
| UF | Indexer | TCP 9997 | `outputs.conf`, receiver stanza, TLS, listener and counters |
| Search Head | Indexer | TCP 8089 | `distsearch.conf`, peer trust and connected status |
| Administrator | Search Head | TCP 8000 | `web.conf`, TLS and access restriction |
| Administrator | Linux nodes | TCP 22 | Existing SSH/OS Login path and firewall scope |

These are conventional ports, not confirmed guest listeners. A firewall allow rule also does not prove a service is listening. Splunk documents these relationships in [Components and their relationship with the network](https://help.splunk.com/?resourceId=Splunk_InheritedDeployment_Ports).

## Boundaries and limitations

One indexer means a single failure domain for indexed data and search availability. All nodes share one zone and the default VPC. No replication factor, search factor, cluster manager, deployer or load balancer has been evidenced. Use a dedicated network, scoped access, verified transport encryption and tested backups for a future redesign; do not apply changes to the preserved lab without approval.

Keep the observed design separate from proposed improvements. This repository does not include an automatic deployment or teardown command.
