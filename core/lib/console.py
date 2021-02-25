import os

from colorama import Fore, Style
from dotenv import load_dotenv
from iptools import IpRangeList
from core.lib import data

load_dotenv(".env")

BANNER = f'''
▄▄▄█████▓ ▒█████   █    ██    ▓█████▄  ▒█████   █    ██  ███▄ ▄███▓    ▐██▌ 
▓  ██▒ ▓▒▒██▒  ██▒ ██  ▓██▒   ▒██▀ ██▌▒██▒  ██▒ ██  ▓██▒▓██▒▀█▀ ██▒    ▐██▌ 
▒ ▓██░ ▒░▒██░  ██▒▓██  ▒██░   ░██   █▌▒██░  ██▒▓██  ▒██░▓██    ▓██░    ▐██▌ 
░ ▓██▓ ░ ▒██   ██░▓▓█  ░██░   ░▓█▄   ▌▒██   ██░▓▓█  ░██░▒██    ▒██     ▓██▒ 
  ▒██▒ ░ ░ ████▓▒░▒▒█████▓    ░▒████▓ ░ ████▓▒░▒▒█████▓ ▒██▒   ░██▒    ▒▄▄  
  ▒ ░░   ░ ▒░▒░▒░ ░▒▓▒ ▒ ▒     ▒▒▓  ▒ ░ ▒░▒░▒░ ░▒▓▒ ▒ ▒ ░ ▒░   ░  ░    ░▀▀▒ 
    ░      ░ ▒ ▒░ ░░▒░ ░ ░     ░ ▒  ▒   ░ ▒ ▒░ ░░▒░ ░ ░ ░  ░      ░    ░  ░ 
  ░      ░ ░ ░ ▒   ░░░ ░ ░     ░ ░  ░ ░ ░ ░ ▒   ░░░ ░ ░ ░      ░          ░ 
             ░ ░     ░           ░        ░ ░     ░            ░       ░    
                               ░                
                    ---===[Author: @MsterHuj]===---
                          --==[Ver : {os.environ.get("APP_VERSION")}]==--
'''


def banner():
    print(Fore.GREEN + Style.BRIGHT + BANNER + Fore.RESET)


def scan_config(ips: IpRangeList, timeout, scan_used, scan_private, output, verbose, threads):
    print("=" * 56)
    print("Ip range            : " + str(ips))
    print("Numbers of ip       : " + str(len(ips)))
    print("Scan service        : " + str(scan_used))
    print("Timeout             : " + str(timeout))

    if output is not None:
        print("|" + "-"*40)
        print("|Output file name    : " + output)
        botnet = data.load(output)
        print("|Vuln server on file")
        print("| > Memcached        : " + str(len(botnet.memcached)))
        print("| > DNS              : " + str(len(botnet.dns)))
        print("| > NTP              : " + str(len(botnet.ntp)))
        print("|" + "-"*40)

    print("Threads             : " + str(threads))
    print("Scan private range  : " + str(scan_private))
    print("Verbose             : " + str(verbose))
    print("=" * 56)


def ip_found(ip: str, service: str):
    print(Fore.GREEN + "[" + service + "] " + Fore.YELLOW + ip + Fore.RESET)


def ip_not_found(ip: str, service: str):
    print(Fore.RED + "[" + service + "] " + Fore.YELLOW + ip + Fore.RESET)


def ip_skipped(ip: str):
    print(Fore.YELLOW + "Skipped private ip " + ip + Fore.RESET)


def error(msg: str):
    print(Fore.RED + "[*] " + Fore.RESET + "Error : " + msg)
