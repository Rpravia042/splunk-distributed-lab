# Example distributed lab health dashboard

This example adds available disk space, ingestion delay and source delivery status to a CPU and RAM dashboard. The shell collector emits a single key-value line and accepts the directory whose filesystem should be measured.

The example dashboard assumes the index `example_ops`, sourcetype `example:metrics` and expected host `example-forwarder`. Substitute your own names consistently. Set up your input to record one event per run, preserve the event timestamp and run the collector as an unprivileged service account. A run every five minutes fits the example's delivery threshold of twelve minutes.

Copy the XML into a Classic Dashboard in Splunk and run the freshness search independently. Confirm that the expected host appears even when it sends no samples. With synthetic events, verify that the same sample supplies the index-time freshness and the derived delay. Compare the displayed available GiB with the operating system for the configured path. These files provide a template. Actual SPL results depend on your index, extraction and forwarding settings.

Run [synthetic_auth_detection.spl](synthetic_auth_detection.spl) as a standalone search. It generates three fictional scenarios in memory. Only `demo-a` on `workstation-1` reaches five failures in ten minutes. The search should return one row. There is no scheduled alert or real authentication data in this exercise.

The ingestion delay chart groups events by when they arrive at the index, so a replay of older data remains visible even when the event times fall outside the CPU and RAM chart window.

## Schedule the synthetic alert

1. Select an unused private lookup filename and use it consistently in both SPL files. [The seed search](seed_synthetic_auth_lookup.spl) writes or replaces **only** the chosen fixture. It places fixed synthetic timestamps immediately before a five-minute boundary. Do not schedule the seed.
2. Save [the detection search](scheduled_auth_alert.spl) as a private scheduled alert in the same user and app context. Use `*/5 * * * *`, trigger once when **Number of Results > 0**, and select **Add to Triggered Alerts**. The rule reads up to 15 minutes of fixture events and only reports a fifth failure that occurred in the previous five minutes. It uses the lookup's epoch timestamps, independently of the search page's time picker.
3. Run the seed after saving the alert to repeat the exercise. Wait for the scheduler rather than using a manual run as evidence. Check Triggered Alerts and open View Results. Expect one row for `demo-a` with five failures. Later runs age out that fixed batch. The other cases cover four failures followed by success, and five failures spread over twelve minutes.

This alert uses a private CSV lookup and works independently of a log index. A future Python exercise can generate or validate the same fictional input. Map `login_failed` and `login_success` from its JSON Lines schema to `failure` and `success` in the fixture, retaining the event timestamp and source label. Keep the fixture separate from real login records.

For scheduled checks of Forwarder silence and available capacity on the Search Head and Indexer, see [the health alerts and synthetic tests](health-alerts/README.md).

For alerting that works while the Search Head cannot dispatch searches, see [the Cloud Monitoring disk policies and validation guide](cloud-monitoring/README.md).
