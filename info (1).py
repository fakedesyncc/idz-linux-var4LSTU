import GPUtil
import math 
import netifaces
import requests
import datetime as DT
import os
import datetime
import sqlite3
from pathlib import Path
from subprocess import Popen, PIPE, DEVNULL
gpus = GPUtil.getGPUs()
def command(command):
    process = Popen(command, stdout=PIPE, universal_newlines=True, shell=True,stderr=DEVNULL)
    stdout, stderr = process.communicate()
    del stderr
    return stdout
os_file = "/etc/os-release"
os_name = command(("cat "+os_file+" | grep 'PRETTY_NAME'")).replace("PRETTY_NAME=", "").replace('''"''', "").strip()
product_info = command("cat /sys/devices/virtual/dmi/id/product_version").strip()
cpu_info = command("cat /proc/cpuinfo | grep 'model name'").split('\n')[0].replace("model name	: ","").replace("Core(TM)","").replace("(R)","").replace("CPU","").replace("  "," ").split('@')[0]
kernel = command("uname -sro").strip()
for gpu in gpus:
    gpu = gpu.name
mem = int(command("cat /proc/meminfo | grep MemTotal").replace('MemTotal:', "").replace('kB', "").strip())
mem = math.ceil( mem / 1024 / 1024)
wifi_name = command("nmcli -t -f name connection show --active").strip().split("\n")[0]
install_programm = command('ls /usr/bin').strip()
dirs = command("ls ~").strip().split("\n")
ip = requests.get('https://ifconfig.me/ip').text
host = command("cat /etc/hostname")


os.makedirs('resuit', exist_ok=True)


with open("resuit/os.txt", "w") as file:
    file.write(f'[OS info] \n\n')
    file.write(f'System: {os_name} \n')
    file.write(f'Kernel: {kernel}\n')
    file.write(f'Time: {datetime.datetime.now()}\n')
    file.write(f'Hostname: {host}\n\n')
    file.write(f'[Hardware info] \n\n')
    file.write(f'CPU: {cpu_info}\n')
    file.write(f'GPU: {gpu}\n')
    file.write(f'Memory: {mem} GB \n\n')
    file.write(f'[Disk Info]\n\n')
    file.write(F'{command("df -BG")} \n')

with open("resuit/network.txt", "w") as file:
    file.write(f'[Network Info]\n\n')
    file.write(f'IP: {ip}\n')
    file.write(f'Wifi name connect: {wifi_name} \n')
    for el in netifaces.interfaces():
        file.write(f'Name: {el}\n')
        net = netifaces.ifaddresses(el)
        for el2 in net:
            addr = net[el2][0]['addr']
            try:
                mask = net[el2][0]['netmask']
            except KeyError:
                mask = "none"
            file.write(f'Addr: { addr }\n')
            file.write(f'Netmask: { mask }\n\n')
with open("resuit/files.txt", "w") as file:
    file.write(f'[File info] \n\n')
    for el in dirs:
        file.write("\n")
        file.write(f'Directory content: {el}\n\n')
        file.write(command(f'ls ~/{el}\n'))
with open("resuit/programs.txt", "w") as file:
    file.write(f'[Installed Programm]\n\n')
    file.write(f'{command("ls /usr/share/applications/").replace(".desktop", "").replace("org.kde.", "")}\n\n')

            
