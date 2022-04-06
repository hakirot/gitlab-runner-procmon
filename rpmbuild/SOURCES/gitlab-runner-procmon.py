#!/usr/bin/python3

import os
import time
import subprocess

procmon_script = """#!/usr/bin/python3

import os
import psutil
import time
import subprocess
import sys

# Grabs the PID of the packer process also spawned by the parent of this process
def get_target_PID(start_time, ppid):

    target_pid      = None
    pprocess        = psutil.Process(int(PPid)) # get parent process info
    search_command  = f'pgrep -P {ppid} packer'

    # Giving the entire timeout to fine an instance of packer, plus 60 seconds
    job_timeout = int(os.environ.get('CI_JOB_TIMEOUT')) + 60

    elapsed_time = time.time() - start_time

    while elapsed_time < job_timeout:

        # Quit if cancelled
        if not pprocess.is_running():
            print(f"procmon: Parent shell {ppid} ended.")
            exit()

        # Run a search and find the packer process with the same PPID as this script
        target_pid = subprocess.run(search_command, shell=True, stdout=sibprocess.PIPE).stdout.decode('utf-8').strip()

        if target_pid:
            return target_pid

        # try again in ten seconds
        time.sleep(10)
        elapsed_time = time.time() - start_time

def terminate_process(pid):

    try:
        process = psutil.Process(int(pid))
        process.terminate()
        print(f"procmon: Process with PID {pid} terminated.")
    except psutil.NoSuchProcess:
        print(f"procmon: No process found with PID {pid}.")

# checks if target process still exists
def process_exists(pid):

    try:
        process =   psutil.Process(int(pid))

    except:
        print(f"procmon: Process {pid} ended.")
        exit

# Tracks the status of packer PID
def watch(target_PID, start_time, ppid):

    # Giving these instances an extra 2 minutes to live..
    termination_time = int(os.environ.get('CI_JOB_TIMEOUT')) + 120

    while True:

        shell_proc   = psutil.Process(int(ppid))
        elapsed_time = time.time() - start_time

        process.exists(target_PID)

        # Check if job timed out or was cancelled
        # If the job was cancelled in gitlab, the shell_proc parent is
        # terminated. Shell proc will be inherited by the OS and given
        # a ppid of '1'
        if elapsed_time > termination_time or shell_proc.ppid() is 1:
            terminate_process(target_PID)
            break

        time.sleep(2)

if __name__ == "__main__":
    if 'CI_JOB_TIMEOUT' not in os.environ:
        print('Error: Not a GitLab CI Job')
        exit()

    start_time =    time.time()
    target_pid = get_target_PID(start_time, sys.argv[1])
    watch(target_pid, start_time, sys.argv[1])
"""

if __name__ == "__main__":
    fd = open("procmon.py", "w")
    fd.write(procmon_script)
    fd.close()

    os.chmod("./procmon.py", 0o755)

    ppid = os.getppid()
    subprocess.run(
        f"nohup ./procmon.py {ppid} > /dev/null 2>&1 &",
        shell=True
    )

    # Provide a moment for procmon script to start since previous os command is async
    time.sleep(2)
    # Process file can be cleaned after being loaded into memory
    os.remove("./procmon.py")
