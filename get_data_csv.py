#!/usr/bin/env python3
 
import requests
import csv
import datetime
import time  #  for some magic reason cant get minutes from datetime

victoriametrics_url = "http://localhost:8428/api/v1/query_range"

csv_file = "./metrics_data.csv"



def query_victoriametrics(metric_name, start, end):
    query_params = {
        "query": metric_name,
        "start": start,
        "end": end,
        "step": "60" 
    }

    response = requests.get(victoriametrics_url, params=query_params)
    if response.status_code == 200:
        return response.json()["data"]["result"]
    else:
        raise Exception(f"Failed to query VictoriaMetrics: {response.status_code}, {response.text}")


def save_metrics_to_csv(metrics_data):
    with open(csv_file, mode="w", newline="") as file:
        csv_writer = csv.writer(file)
        
        csv_writer.writerow(["DateTime", "CPU (%)", "Memory (%)", "HDD (%)"])
        
        for timestamp, cpu, mem, hdd in metrics_data:
            # Convert Unix timestamp to readable DateTime
            dt = datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
            csv_writer.writerow([dt, cpu, mem, hdd])


        print(f"Metrics successfully written to {csv_file}")
    file.close()   


def fetch_and_save_metrics():
    # Get current time and calculate start and end times (past hour)
    end_time = datetime.datetime.now()
    start_time = end_time - datetime.timedelta(hours=1)
    
    # Convert to Unix timestamp format (in seconds)
    start_ts = int(start_time.timestamp())
    end_ts = int(end_time.timestamp())

    # Query VictoriaMetrics for CPU, memory, and disk usage data
    cpu_data = query_victoriametrics("system_cpu_usage_percent", start_ts, end_ts)
    mem_data = query_victoriametrics("system_memory_usage_percent", start_ts, end_ts)
    hdd_data = query_victoriametrics("system_disk_usage_percent", start_ts, end_ts)

    # Prepare data for CSV file (timestamp, cpu, mem, hdd)
    metrics_data = []
    for cpu_point, mem_point, hdd_point in zip(cpu_data[0]["values"], mem_data[0]["values"], hdd_data[0]["values"]):
        timestamp = int(cpu_point[0])
        cpu = float(cpu_point[1])
        mem = float(mem_point[1])
        hdd = float(hdd_point[1])
        metrics_data.append((timestamp, cpu, mem, hdd))

    # Save the data to CSV
    save_metrics_to_csv(metrics_data)



if __name__ == "__main__":
    fetch_and_save_metrics()



