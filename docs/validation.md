# Validation plan and results

**No live checks have passed yet.** The VMs were stopped during inspection. Repository checks are independent of the following deployment checks.

| ID | Check | Evidence required for PASS | Current result |
| --- | --- | --- | --- |
| V01 | Version and service identity | Node, version/build, service unit and process owner | Pending guest access |
| V02 | UF inputs | Reviewed source stanza, readable source file, intended index/sourcetype | Pending |
| V03 | UF destination | Effective outputs and active connection to the intended indexer | Pending |
| V04 | Indexer receiver | Effective receiver stanza, listener and receiving counters/logs | Pending |
| V05 | Index routing | Index exists, storage paths/permissions and observed events in it | Pending |
| V06 | Distributed search | Peer status on SH and query results from the intended indexer | Pending |
| V07 | End-to-end visibility | Existing known event found through SH, time range and source documented | Pending |
| V08 | Time and parsing | Event time, host, source, sourcetype and expected fields inspected | Pending |
| V09 | Transport protection | Relevant TLS settings and certificate validation evidence | Pending |
| V10 | Preservation | Required files recovered, gaps reviewed, private backup readable | Incomplete |

## Existing-data searches

Replace `lab` with the **observed** index; it is only a reference name here. Run on the Search Head in an authorized session. Bound the time range to the original activity, and record both timezone and query interval. An empty last-24-hour search can be expected for a stopped lab.

```spl
index=lab earliest=-24h latest=now
| stats count min(_time) AS first_event max(_time) AS last_event
    by host source sourcetype splunk_server
| convert ctime(first_event) ctime(last_event)
```

To inspect metadata without publishing raw event content:

```spl
index=lab earliest=-24h latest=now
| head 20
| table _time host source sourcetype splunk_server
```

`splunk_server` identifies the search peer associated with events; see [Splunk's distributed-peer search guidance](https://help.splunk.com/en/splunk-enterprise/search/search-manual/10.2/retrieve-events/search-across-one-or-more-distributed-search-peers). It does not alone establish loss-free ingestion or durability.

## Result record

Each record needs: check ID, UTC capture time, node, command/query, time range, expected result, actual result, PASS/FAIL/BLOCKED, limitations and reviewed evidence path. Preserve failure output privately; redact before publication. Do not mark a query as passed merely because the search UI opened.

End-to-end testing with a newly generated marker modifies source data and Splunk indexes. It requires separate authorization if existing data cannot demonstrate the path.
