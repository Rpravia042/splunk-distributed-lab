# Personal Splunk lab

Three installable app directories implement a capacity and ingestion pilot for new, isolated Linux nodes. The Search Head dashboard shows available GiB, missing forwarder samples and 95th-percentile ingestion delay. The explicit expected-host row keeps silent sources visible. Samples are collected once per minute; after three minutes a host is late. If no event is found in the 15-minute search window, the dashboard reports a missing sample.

## Local verification

From the repository root run `python3 -m unittest discover -s tests -v`. On macOS or Linux run `python3 personal-lab/apps/personal_ops_uf/bin/capacity.py .` for one JSON sample. The pilot warns below 6 GiB of available disk space. The original Search Head incident measured 4,799,356,928 bytes before repair and 15,011,602,432 after repair. This dashboard measures the filesystem containing the personal forwarder's installation; to monitor dispatch or index storage, instrument the corresponding filesystem on that role and include that host in the dashboard’s expected hosts.

## Personal deployment and acceptance

1. Use fresh Splunk identities, synchronized clocks and new TLS trust on the three personal hosts. Set the input host to personal-uf and the indexer's Splunk server name to personal-idx. Set up private, certificate-verified UF forwarding and SH distributed search. These apps supply monitoring after those connections exist.
2. Copy personal_ops_idx to the personal indexer's etc/apps directory; apply the app and verify the personal_ops index exists. Retention is limited to seven days or 1024 MB. Copy personal_ops_sh to the personal Search Head's etc/apps; apply it and open Personal Lab Health.
3. Copy personal_ops_uf to the personal forwarder's etc/apps; preserve executable permissions on bin/collect.sh. Confirm /usr/bin/python3 exists, the service account can read the app, and the receiver is ready before enabling the app. Apply the configuration using the personal node's service manager. Inspect effective settings with Splunk btool.
4. Generate a unique label on the personal UF with `python3 -c 'import uuid; print(uuid.uuid4())'`. Write down the resulting UUID. Emit one JSON event by running the following as the personal forwarder's service account from an installation with SPLUNK_HOME set. Replace YOUR_UUID with the generated UUID. Install the one-shot file outside previously monitored paths and use a new filename each run.

   ```sh
   id=YOUR_UUID
   scratch=$(mktemp -d)
   sample="$scratch/probe-$id.json"
   python3 "$SPLUNK_HOME/etc/apps/personal_ops_uf/bin/capacity.py" "$SPLUNK_HOME" |
     python3 -c 'import json,sys; e=json.load(sys.stdin); e["probe_id"]=sys.argv[1]; print(json.dumps(e))' "$id" > "$sample"
   "$SPLUNK_HOME/bin/splunk" add oneshot "$sample" -index personal_ops -sourcetype personal:capacity -host personal-uf
   ```

5. Run the following search from the personal Search Head within 15 minutes, replacing YOUR_UUID with the same value. Expect exactly one event on the row personal-uf / personal-idx. Record the result and time. Then stop just the personal UF; verify Late after three minutes and Reporting after restarting it. Records take time to arrive. Keep the Indexer and Search Head running during the test.

   ```spl
   index=personal_ops sourcetype=personal:capacity earliest=-15m "YOUR_UUID"
   | spath
   | search probe_id="YOUR_UUID"
   | stats count by host splunk_server
   ```

See [the GCP pilot plan](piloto-gcp.md). Cloud deployment, SPL runtime behavior and end-to-end results require verification on the personal nodes.
