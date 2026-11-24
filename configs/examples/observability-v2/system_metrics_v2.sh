#!/bin/bash
# One key=value sample on stdout. Pass the directory on the filesystem to measure.
set -eu
export LC_ALL=C
timestamp=$(date --iso-8601=seconds)
cpu_usage=$(top -bn2 -d 1 | awk '/Cpu\(s\)/ {idle=$8; found=1} END {if (!found) exit 1; printf "%.2f", 100-idle}')
ram_usage=$(free | awk '/^Mem:/ && $2>0 {printf "%.2f", $3/$2*100; found=1} END {if (!found) exit 1}')
disk=$(df -Pk -- "${1:-.}" | awk 'NR==2 {sub(/%$/, "", $5); printf "disk_available_kib=%s disk_used_pct=%s", $4, $5; found=1} END {if (!found) exit 1}')
read -r load1 _ </proc/loadavg
read -r uptime _ </proc/uptime
swap=$(free -k | awk '/^Swap:/ {printf "swap_total_kib=%s swap_used_kib=%s", $2, $3; found=1} END {if (!found) exit 1}')
printf 'timestamp=%s cpu_usage=%s ram_usage=%s %s load_1m=%s uptime_seconds=%s %s metrics_version=2\n' "$timestamp" "$cpu_usage" "$ram_usage" "$disk" "$load1" "${uptime%%.*}" "$swap"
