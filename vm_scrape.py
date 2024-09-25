import psutil
import datetime
import requests

pushgateway_url = "http://localhost:8428/api/v1/import/prometheus"

def collect_system_stats():
    now = datetime.datetime.now(datetime.UTC)
    cpu_usage = psutil.cpu_percent(interval=1)

    # Get memory usage
    mem_info = psutil.virtual_memory()
    mem_usage = mem_info.percent

    # Get disk usage
    disk_usage = psutil.disk_usage('/').percent

    # Format the data in Prometheus format
    metrics_data = f"""
    system_cpu_usage_percent {cpu_usage}
    system_memory_usage_percent {mem_usage}
    system_disk_usage_percent {disk_usage}
    system_stats_timestamp "{now}"
    """

    # Send the data to VictoriaMetrics Pushgateway
    response = requests.post(pushgateway_url, data=metrics_data)

    # Check if the data was successfully sent
    if response.status_code == 200:
        print("Metrics successfully sent to VictoriaMetrics.")
    else:
        print(f"Failed to send metrics: {response.status_code}, {response.text}")

if __name__ == "__main__":
    collect_system_stats()
