# References

Consulted 2026-11-03. Installed Splunk versions are not yet known; use the matching version of each reference before applying configuration.

- [Splunk: components and network relationships](https://help.splunk.com/?resourceId=Splunk_InheritedDeployment_Ports) — conventional component ports.
- [Splunk: use btool to troubleshoot configurations](https://help.splunk.com/en/splunk-enterprise/administer/troubleshoot/9.3/first-steps/use-btool-to-troubleshoot-configurations) — inspect merged settings and source paths. Disk configuration does not prove the running service has loaded it.
- [Splunk: add search peers](https://help.splunk.com/en/splunk-enterprise/administer/distributed-search/9.0/deploy-distributed-search/add-search-peers-to-the-search-head) — peer setup and authentication context; do not copy credential-bearing command examples into shell history.
- [Splunk: search across distributed peers](https://help.splunk.com/en/splunk-enterprise/search/search-manual/10.2/retrieve-events/search-across-one-or-more-distributed-search-peers) — interpreting `splunk_server`.

Console observations are recorded separately in the evidence register. Documentation describes product behavior, not proof that the original deployment implements it.

Repository automation uses the official [actions/checkout source pinned by commit](https://github.com/actions/checkout/tree/11bd71901bbe5b1630ceea73d27597364c9af683), with credential persistence disabled and read-only repository permissions. It has no Google Cloud credentials or deployment step.
