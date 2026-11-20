"""Emit one filesystem capacity sample for the personal Splunk lab."""
import argparse
from datetime import datetime, timezone
import json
import os
import sys


def capacity_state(available_bytes):
    # Early warning for the pilot, independent of Splunk's configured limit.
    return "warning" if available_bytes < 6 * 1024**3 else "ok"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", help="An existing directory on the filesystem to measure")
    args = parser.parse_args()
    if not os.path.isdir(args.path):
        parser.error("Select an existing, accessible directory.")
    try:
        fs = os.statvfs(args.path)
    except OSError as exc:
        print(f"Capacity unavailable: {exc.strerror}", file=sys.stderr)
        return 1
    available = fs.f_bavail * fs.f_frsize
    print(json.dumps({
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S%z"),
        "available_bytes": available,
        "capacity_state": capacity_state(available),
    }))
    return 0


if __name__ == "__main__":
    sys.exit(main())
