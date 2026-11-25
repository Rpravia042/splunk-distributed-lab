# Scheduled health checks

These examples distinguish a missing Forwarder sample from missing telemetry on the receiving side. Substitute the example host names, index and sourcetype. Before using the capacity check, confirm the actual filesystem for the dispatch directory and for the index volumes. The example assumes one mount per role. Check the effective Splunk free-space limit before using the example thresholds.

| Search | Cron | Trigger | Suppression |
| --- | --- | --- | --- |
| [Forwarder silence](forwarder_silent.spl) | `*/5 * * * *` | More than 12 minutes since the last eligible indexed sample, or no sample found. | 60 minutes per host and diagnostic status |
| [Disk capacity](disk_capacity.spl) | `*/10 * * * *` | Available capacity below 6 GiB or a missing reading for a configured mount. | 120 minutes per server, mount and status |

Save both alerts privately. Trigger when the number of results is greater than zero, select **For each result** and set **Add to Triggered Alerts** as the only action. The Forwarder search combines index time, internal metrics and REST observations. An enabled input is configuration evidence. Confirm an actual listener and connection independently before concluding that the receiver is healthy. A late event may also come from a clock discrepancy.

[The Forwarder fixture](test_forwarder_silent.spl) should return five diagnosis rows. It excludes both a recent sample and the exact 720-second boundary. [The disk fixture](test_disk_capacity.spl) should return two rows, low disk and missing telemetry. It excludes capacity at exactly 6 GiB. Run the fixtures manually, then run the environment-specific live searches and record the expected result. Neither fixture changes any service or disk.

Check fresh samples and a subsequent successful scheduled execution with zero results after remediation. An automated recovery notice requires independent state for each server and mount. This check runs in Splunk and needs an external signal if the Search Head itself can no longer dispatch searches.

[Disk introspection reference](https://help.splunk.com/en/splunk-enterprise/rest-api-reference/10.0/introspection-endpoints/introspection-endpoint-descriptions) · [Scheduled search settings](https://help.splunk.com/en/splunk-enterprise/administer/admin-manual/10.6/configuration-file-reference/10.6.0-configuration-file-reference/savedsearches.conf)
