# References

Consulted 2026-11-03. Recovered metadata reports Splunk 10.6.1.1. References explain concepts; select matching product documentation and verify OS support before a rebuild.

- [Splunk: components and network relationships](https://help.splunk.com/?resourceId=Splunk_InheritedDeployment_Ports) — conventional component ports.
- [Splunk: use btool to troubleshoot configurations](https://help.splunk.com/en/splunk-enterprise/administer/troubleshoot/9.3/first-steps/use-btool-to-troubleshoot-configurations) — inspect merged settings and source paths. Disk configuration does not prove the running service has loaded it.
- [Splunk: add search peers](https://help.splunk.com/en/splunk-enterprise/administer/distributed-search/9.0/deploy-distributed-search/add-search-peers-to-the-search-head) — peer setup and authentication context; do not copy credential-bearing command examples into shell history.
- [Splunk: search across distributed peers](https://help.splunk.com/en/splunk-enterprise/search/search-manual/10.2/retrieve-events/search-across-one-or-more-distributed-search-peers) — interpreting `splunk_server`.

Console observations are recorded separately in the evidence register. Documentation describes product behavior, not proof that the original deployment implements it.

Repository automation uses the official [actions/checkout source pinned by commit](https://github.com/actions/checkout/tree/11bd71901bbe5b1630ceea73d27597364c9af683), with credential persistence disabled and read-only repository permissions. It has no Google Cloud credentials or deployment step.

- [Export data using Splunk Web](https://help.splunk.com/en/splunk-cloud-platform/search/search-manual/9.3.2411/export-search-results/export-data-using-splunk-web): formats and rerun behavior for results not stored in the job artifact.
- [Google Cloud: resize a Persistent Disk](https://docs.cloud.google.com/compute/docs/disks/resize-persistent-disk), consulted 2026-11-07: disk capacity, partition and filesystem are separate layers; describes online XFS growth after partition expansion.
