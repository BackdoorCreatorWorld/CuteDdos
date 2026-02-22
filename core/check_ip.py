#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Check Real IP Utility
Architect 01 - Professional Suite
"""

import requests
import json
from colorama import Fore, Style

def check_real_ip():
    """
    Check the real public IP address
    Uses multiple services for verification
    """
    print(Fore.YELLOW + "\n╰─❯ Checking your real IP address...\n" + Style.RESET_ALL)
    
    services = [
        ('https://api.ipify.org?format=json', 'ipify'),
        ('https://httpbin.org/ip', 'httpbin'),
        ('https://api.myip.com', 'myip'),
    ]
    
    ips = []
    
    for url, name in services:
        try:
            response = requests.get(url, timeout=10)
            data = response.json()
            
            if name == 'ipify':
                ip = data.get('ip')
            elif name == 'httpbin':
                ip = data.get('origin')
            elif name == 'myip':
                ip = data.get('ip')
            else:
                ip = None
            
            if ip:
                ips.append(ip)
                print(Fore.GREEN + "╰─❯ " + name + ": " + ip + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + "╰─❯ " + name + ": Failed - " + str(e)[:30] + Style.RESET_ALL)
    
    if ips:
        unique_ips = set(ips)
        if len(unique_ips) == 1:
            print(Fore.GREEN + "\n╰─❯ ✓ Your real IP is: " + list(unique_ips)[0] + Style.RESET_ALL)
        else:
            print(Fore.YELLOW + "\n╰─❯ ⚠ Inconsistent IPs detected!" + Style.RESET_ALL)
    
    print(Fore.CYAN + "\n╰─❯ DNS Leak Test:" + Style.RESET_ALL)
    try:
        import socket
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        print(Fore.CYAN + "╰─❯ Hostname: " + hostname + Style.RESET_ALL)
        print(Fore.CYAN + "╰─❯ Local IP: " + local_ip + Style.RESET_ALL)
    except:
        print(Fore.RED + "╰─❯ Could not determine local IP" + Style.RESET_ALL)
    
    print(Fore.YELLOW + "\n╰─❯ Press Enter to continue..." + Style.RESET_ALL)
    input()
