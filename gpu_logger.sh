#!/bin/bash

INTERVAL=60  # Interval in seconds
LOG_DIR="$(pwd)/GPU_Usage_Logs"
mkdir -p "$LOG_DIR"

log_gpu_usage() {
    timestamp=$(date +"%Y-%m-%d %H:%M:%S")
    date_day=$(date +"%Y-%m-%d")
    date_week=$(date +"%Y-%V")
    date_month=$(date +"%Y-%m")

    daily_log="$LOG_DIR/gpu_usage_daily_$date_day.csv"
    weekly_log="$LOG_DIR/gpu_usage_weekly_$date_week.csv"
    monthly_log="$LOG_DIR/gpu_usage_monthly_$date_month.csv"

    # Write CSV header if file doesn't exist
    for file in "$daily_log" "$weekly_log" "$monthly_log"; do
        if [ ! -f "$file" ]; then
            echo "Timestamp,GPU Index,GPU Name,Utilization,Memory Used,Memory Total (MiB)" > "$file"
        fi
    done

    nvidia-smi --query-gpu=index,name,utilization.gpu,memory.used,memory.total \
        --format=csv,noheader,nounits | while IFS=',' read -r index name util_gpu mem_used mem_total; do
        output="$timestamp,$index,$name,$util_gpu,$mem_used,$mem_total"
        echo "$output" >> "$daily_log"
        echo "$output" >> "$weekly_log"
        echo "$output" >> "$monthly_log"
    done
}

echo "Starting Minimal GPU Logger..."
echo "Log directory: $LOG_DIR"
echo "Interval: $INTERVAL seconds"
echo "Press Ctrl+C to stop"

while true; do
    log_gpu_usage
    sleep $INTERVAL
done