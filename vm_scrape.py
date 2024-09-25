#!/usr/bin/env python3

import psutil
import datetime
import requests

pushgateway_url = "http://localhost:8428/api/v1/import/prometheus"

def collect_system_stats():
    now = datetime.datetime.now(datetime.UTC)
    cpu_usage = psutil.cpu_percent(interval=1)

    mem_info = psutil.virtual_memory()
    mem_usage = mem_info.percent

    disk_usage = psutil.disk_usage('/').percent

    metrics_data = f"""
    system_cpu_usage_percent {cpu_usage}
    system_memory_usage_percent {mem_usage}
    system_disk_usage_percent {disk_usage}
    system_stats_timestamp "{now}"
    """

    response = requests.post(pushgateway_url, data=metrics_data)

    if response.status_code == 200:
        print("Metrics successfully sent to VictoriaMetrics.")
    else:
        print(f"Failed to send metrics: {response.status_code}, {response.text}")   # In my case returns code 204. No solutions found

if __name__ == "__main__":
    collect_system_stats()
