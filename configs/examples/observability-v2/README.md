# Example distributed lab health dashboard

This example adds available disk space, ingestion delay and source delivery status to a CPU and RAM dashboard. The shell collector emits a single key-value line and accepts the directory whose filesystem should be measured.

The example dashboard assumes the index `example_ops`, sourcetype `example:metrics` and expected host `example-forwarder`. Substitute your own names consistently. Set up your input to record one event per run, preserve the event timestamp and run the collector as an unprivileged service account. A run every five minutes fits the example's delivery threshold of twelve minutes.

Copy the XML into a Classic Dashboard in Splunk and run the freshness search independently. Confirm that the expected host appears even when it sends no samples. With synthetic events, verify that the same sample supplies the index-time freshness and the derived delay. Compare the displayed available GiB with the operating system for the configured path. These files provide a template. Actual SPL results depend on your index, extraction and forwarding settings.

Run [synthetic_auth_detection.spl](synthetic_auth_detection.spl) as a standalone search. It generates three fictional scenarios in memory. Only `demo-a` on `workstation-1` reaches five failures in ten minutes. The search should return one row. There is no scheduled alert or real authentication data in this exercise.

The ingestion delay chart groups events by when they arrive at the index, so a replay of older data remains visible even when the event times fall outside the CPU and RAM chart window.
