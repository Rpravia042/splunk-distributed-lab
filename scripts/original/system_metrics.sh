#!/bin/bash

timestamp=$(date --iso-8601=seconds)

cpu_usage=$(LC_ALL=C top -bn2 -d 1 | awk '/Cpu\(s\)/ {idle=$8} END {printf "%.2f", 100-idle}')

ram_usage=$(free | awk '/Mem:/ {printf "%.2f", ($3/$2)*100}')

echo "timestamp=$timestamp cpu_usage=$cpu_usage ram_usage=$ram_usage"
