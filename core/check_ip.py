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
    print(f"{Fore.YELLOW}\n   ╰─❯ Checking your real IP address...{Style.RESET_ALL}\n")
    
    services = [
        ('https://api.ipify.org?format=json', 'ipify'),
        ('https://httpbin.org/ip', 'httpbin'),
        ('https://api.myip.com', 'myip'),
        ('https://ipapi.co/json/', 'ipapi')
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
            elif name == 'ipapi':
                ip = data.get('ip')
            else:
                ip = None
            
            if ip:
                ips.append(ip)
                print(f"{Fore.GREEN}   ╰─❯ {name}: {ip}{Style.RESET_ALL}")
                
        except Exception as e:
            print(f"{Fore.RED}   ╰─❯ {name}: Failed - {str(e)[:30]}{Style.RESET_ALL}")
    
    # Check if all IPs match
    if ips:
        unique_ips = set(ips)
        if len(unique_ips) == 1:
            print(f"\n{Fore.GREEN}   ╰─❯ ✓ Your real IP is: {list(unique_ips)[0]}{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.YELLOW}   ╰─❯ ⚠ Inconsistent IPs detected!{Style.RESET_ALL}")
            for i, ip in enumerate(ips):
                print(f"{Fore.YELLOW}      {i+1}. {ip}{Style.RESET_ALL}")
    
    # Check DNS
    print(f"\n{Fore.CYAN}   ╰─❯ DNS Leak Test:{Style.RESET_ALL}")
    try:
        import socket
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        print(f"{Fore.CYAN}   ╰─❯ Hostname: {hostname}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}   ╰─❯ Local IP: {local_ip}{Style.RESET_ALL}")
    except:
        print(f"{Fore.RED}   ╰─❯ Could not determine local IP{Style.RESET_ALL}")
    
    print(f"\n{Fore.YELLOW}   ╰─❯ Press Enter to continue...{Style.RESET_ALL}")
    input()
