# Configuration provenance

`recovered/` is reserved for sanitized files actually read from the original VMs. No guest files have been recovered yet.

`examples/` contains newly authored, minimal reference snippets. They are **not the original lab configuration** and are not a complete secure deployment. Do not copy them into the preserved lab. The snippets illustrate relationships only; confirm the installed version, storage, license, authentication and TLS before building a separate environment.

For each recovered file record: node, original relative path, capture time, private raw hash, sanitized artifact hash, removed field categories, reviewer and source evidence. Keep private paths, live addresses, original hashes and redaction mappings in `.recovery/`; publish only the sanitized provenance needed by readers.
