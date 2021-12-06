# source: https://www.fosslinux.com/43882/extracting-linux-system-and-hardware-info-using-python.htm

import platform
from datetime import datetime
import psutil
import os

print("[+] Architecture :", platform.architecture()[0])
print("[+] System Name :", platform.system())
print("[+] Operating System Version :", platform.version())
print("[+] Platform :", platform.platform())
print("[+] Processor :", platform.processor())

# getting thesystem up time from the uptime file at proc directory
with open("/proc/uptime", "r") as f:
    uptime = f.read().split(" ")[0].strip()

uptime = int(float(uptime))
uptime_hours = uptime // 3600
uptime_minutes = (uptime % 3600) // 60
print(
    "[+] System Uptime : "
    + str(uptime_hours)
    + ":"
    + str(uptime_minutes)
    + " hours"
)

# number of processes
pids = []
for subdir in os.listdir("/proc"):
    if subdir.isdigit():
        pids.append(subdir)
print("[+] Total number of processes : {0}".format(len(pids)))
print("[+] Number of Physical cores :", psutil.cpu_count(logical=False))
print("[+] Number of Total cores :", psutil.cpu_count(logical=True))

cpu_frequency = psutil.cpu_freq()
print(f"[+] Max Frequency : {cpu_frequency.max:.2f}Mhz")
print(f"[+] Min Frequency : {cpu_frequency.min:.2f}Mhz")
print(f"[+] Current Frequency : {cpu_frequency.current:.2f}Mhz")
print(f"[+] Total CPU Usage : {psutil.cpu_percent()}%")

# reading the cpuinfo file to print the name of
# the CPU present
with open("/proc/cpuinfo", "r") as f:
    file_info = f.readlines()

cpuinfo = [x.strip().split(":")[1] for x in file_info if "model name" in x]
for index, item in enumerate(cpuinfo):
    print("[+] Processor " + str(index) + " : " + item)
# writing a function to convert bytes to GigaByte
def bytes_to_GB(bytes):
    gb = bytes / (1024 * 1024 * 1024)
    gb = round(gb, 2)
    return gb


# Using the virtual_memory() function it will return a tuple
virtual_memory = psutil.virtual_memory()

# This will print the primary memory details
print("[+] Total Memory present :", bytes_to_GB(virtual_memory.total), "Gb")
print(
    "[+] Total Memory Available :", bytes_to_GB(virtual_memory.available), "Gb"
)
print("[+] Total Memory Used :", bytes_to_GB(virtual_memory.used), "Gb")
print("[+] Percentage Used :", virtual_memory.percent, "%")

# This will print the swap memory details if available
swap = psutil.swap_memory()
print(f"[+] Total swap memory : {bytes_to_GB(swap.total)}")
print(f"[+] Free swap memory : {bytes_to_GB(swap.free)}")
print(f"[+] Used swap memory : {bytes_to_GB(swap.used)}")
print(f"[+] Percentage Used : {swap.percent}%")
