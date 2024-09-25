#!/usr/bin/env python3

import os.path
import subprocess
import sys

file = sys.argv[1]  #  Update path || from sys.argv or from input?
script_to_run = 0

def create_cron_job():
    cron_list = subprocess.run(["crontab", "-l"], capture_output=True, text=True)  #  Probably should redo || Usage of subprocess.check.call advised
    
    new_cron_job = f"* * * * * {script_to_run} > /dev/null 2>&1\n"    #  > /dev/null 2>&1\n" added to remove MTA error notification

    # Check if the cron job is already present
    if new_cron_job in cron_list.stdout:
        print("Cron job already exists.")
        return

    updated_cron = cron_list.stdout + new_cron_job

    process = subprocess.run(["crontab", "-"], input=updated_cron, text=True)

    if process.returncode == 0:
        print(f"Cron job added successfully: {new_cron_job.strip()}")
    else:
        print(f"Failed to add cron job. Error code: {process.returncode}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Wrong cl arguments usage")
        exit
    elif os.path.isfile(sys.argv[1]):
        script_to_run = os.path.abspath(sys.argv[1])
        create_cron_job()
    else: print("Specified path is not a file")



