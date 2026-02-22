#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Proxy Manager for DDoS Attacks
Architect 01 - Professional Suite
"""

import random
import requests
import threading
import time

class ProxyManager:
    """Manage proxies for attacks"""
    
    def __init__(self):
        self.proxies = []
        self.current_index = 0
        self.lock = threading.Lock()
        self.load_proxies()
    
    def load_proxies(self):
        """Load proxies from file or create default list"""
        try:
            with open('proxies.txt', 'r') as f:
                self.proxies = [line.strip() for line in f if line.strip()]
            print(f"[✓] Loaded {len(self.proxies)} proxies from file")
        except FileNotFoundError:
            # Default proxies for demo (in real use, you'd have a larger list)
            self.proxies = self.get_default_proxies()
            print(f"[!] No proxies.txt found, using {len(self.proxies)} default proxies")
    
    def get_default_proxies(self):
        """Return some default proxies (should be replaced with real ones)"""
        return [
            'http://185.162.231.111:8080',
            'http://45.67.123.45:8080',
            'http://183.89.45.67:8080',
            'socks5://45.76.187.125:1080',
            'socks4://103.149.162.194:4145',
            'http://103.152.112.120:80',
            'http://27.79.130.155:9090',
            'http://95.216.22.119:3128',
            'socks5://167.99.96.195:1080',
            'http://103.105.39.66:8080'
        ]
    
    def get_random_proxy(self):
        """Return random proxy dictionary for requests"""
        with self.lock:
            if not self.proxies:
                return None
            
            proxy_str = random.choice(self.proxies)
            
            if '://' in proxy_str:
                protocol, address = proxy_str.split('://', 1)
                return {protocol: f'{protocol}://{address}'}
            else:
                # Default to http
                return {'http': f'http://{proxy_str}', 'https': f'http://{proxy_str}'}
    
    def rotate_proxy(self):
        """Rotate to next proxy in list"""
        with self.lock:
            if self.proxies:
                self.current_index = (self.current_index + 1) % len(self.proxies)
                proxy_str = self.proxies[self.current_index]
                
                if '://' in proxy_str:
                    protocol, address = proxy_str.split('://', 1)
                    return {protocol: f'{protocol}://{address}'}
                else:
                    return {'http': f'http://{proxy_str}', 'https': f'http://{proxy_str}'}
        return None
    
    def fetch_new_proxies(self):
        """Fetch fresh proxies from online sources (optional)"""
        # This would scrape proxy sites - for educational purposes only
        # Not implemented in this version to keep it clean
        pass
