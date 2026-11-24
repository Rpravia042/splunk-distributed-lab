#!/bin/sh
# Emit synthetic capacity samples with a shifted timestamp to exercise the
# "Expected forwarders and last sample" table without touching personal-uf.
#
# Usage, on the personal UF as its service account, after `splunk login`:
#   sh sim-panel-cases.sh CASE OFFSET_SECONDS [COUNT]
# Examples:
#   sh sim-panel-cases.sh delay600   -600 6   # steady 10-minute delay
#   sh sim-panel-cases.sh ahead600    600 3   # clock 10 min ahead, then stops
#   sh sim-panel-cases.sh behind1200 -1200 5  # clock 20 min behind
# Events use host sim-CASE, one per minute; search them with the dashboard
# query after replacing "personal-uf" by "sim-CASE". Never change a VM clock.
set -eu
[ $# -ge 2 ] || { echo "usage: $0 CASE OFFSET_SECONDS [COUNT]" >&2; exit 2; }
case_id=$1
offset=$2
count=${3:-1}
case "$case_id" in *[!A-Za-z0-9_-]*|'') echo "CASE: letters, digits, _ or - only" >&2; exit 2;; esac
case "${offset#-}" in *[!0-9]*|'') echo "OFFSET_SECONDS must be an integer" >&2; exit 2;; esac
case "$count" in *[!0-9]*|''|0) echo "COUNT must be a positive integer" >&2; exit 2;; esac
host="sim-$case_id"
dir=$(mktemp -d)
i=0
while [ "$i" -lt "$count" ]; do
  f="$dir/$host-$(date +%s)-$i.json"
  python3 -c 'import json,sys,datetime as d
t=d.datetime.now(d.timezone.utc)+d.timedelta(seconds=int(sys.argv[1]))
print(json.dumps({"timestamp":t.strftime("%Y-%m-%dT%H:%M:%S%z"),"available_bytes":10737418240,"capacity_state":"ok","synthetic":True,"case":sys.argv[2]}))' "$offset" "$case_id" > "$f"
  if [ -n "${SIM_DRY_RUN:-}" ]; then
    cat "$f"
  else
    "${SPLUNK_HOME:?}/bin/splunk" add oneshot "$f" -index personal_ops -sourcetype personal:capacity -host "$host"
  fi
  i=$((i + 1))
  if [ "$i" -lt "$count" ] && [ -z "${SIM_DRY_RUN:-}" ]; then sleep 60; fi
done
echo "Sent $count event(s) as host=$host at $(date -u +%FT%TZ)" >&2
