#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
URL Validator for DDoS Attacks
Architect 01 - Professional Suite
SUPPORT ALL URL TYPES: http, https, ftp, IP, localhost, domain apapun
"""

import re
from urllib.parse import urlparse

def validate_url(url):
    """
    Validate URL format - SUPPORT SEMUA JENIS
    
    Returns:
        tuple: (is_valid, formatted_url, error_message)
    """
    if not url:
        return False, None, "URL cannot be empty"
    
    # Bersihin dulu dari spasi
    url = url.strip()
    
    # Cek kalo udah ada protocol
    if not url.startswith(('http://', 'https://', 'ftp://')):
        # Kalo gak ada, coba detect
        # Cek kalo IP address
        ip_pattern = r'^(\d{1,3}\.){3}\d{1,3}(:\d+)?$'
        if re.match(ip_pattern, url.split('/')[0]):
            url = 'http://' + url
        # Cek kalo localhost
        elif url.startswith('localhost') or url.startswith('127.0.0.1'):
            url = 'http://' + url
        # Cek kalo domain biasa
        elif '.' in url.split('/')[0]:
            url = 'http://' + url
        # Selain itu tetep tambahin http
        else:
            url = 'http://' + url
    
    # Parse URL
    try:
        parsed = urlparse(url)
        
        # Cek kalo kosong
        if not parsed.netloc and not parsed.path:
            return False, None, "Invalid URL format"
        
        # Kalo cuma path doang tanpa netloc, berarti relative URL - TOLAK
        if not parsed.netloc and parsed.path:
            # Coba tambahin dummy host? Gak, better suruh user masukin lengkap
            return False, None, "Relative URL not allowed. Use full URL with domain/IP"
        
        # Validasi IP address kalo ada
        if parsed.netloc:
            host = parsed.netloc.split(':')[0]
            # Cek kalo format IP
            ip_parts = host.split('.')
            if len(ip_parts) == 4 and all(part.isdigit() for part in ip_parts):
                for part in ip_parts:
                    if int(part) > 255:
                        return False, None, "Invalid IP address (octet > 255)"
        
        # SEMUA VALID! Support apapun
        return True, url, None
        
    except Exception as e:
        return False, None, f"URL validation error: {str(e)}"

def get_target_url():
    """
    Prompt user for URL and validate until valid
    
    Returns:
        str: Validated URL
    """
    from colorama import Fore, Style
    
    print(Fore.YELLOW + "\n╰─❯ Supported formats:" + Style.RESET_ALL)
    print(Fore.YELLOW + "    • http://example.com" + Style.RESET_ALL)
    print(Fore.YELLOW + "    • https://example.com" + Style.RESET_ALL)
    print(Fore.YELLOW + "    • example.com (auto-add http)" + Style.RESET_ALL)
    print(Fore.YELLOW + "    • 192.168.1.1 (auto-add http)" + Style.RESET_ALL)
    print(Fore.YELLOW + "    • localhost:8080 (auto-add http)" + Style.RESET_ALL)
    print(Fore.YELLOW + "    • ftp://example.com" + Style.RESET_ALL)
    
    while True:
        print(f"\n{Fore.CYAN}╭─❯ Enter target URL{Style.RESET_ALL}")
        url = input(f"{Fore.CYAN}╰─❯ {Style.RESET_ALL}").strip()
        
        is_valid, formatted_url, error = validate_url(url)
        
        if is_valid:
            print(f"{Fore.GREEN}╰─❯ URL valid: {formatted_url}{Style.RESET_ALL}\n")
            return formatted_url
        else:
            print(f"{Fore.RED}╰─❯ Error: {error}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}╰─❯ Please enter a valid URL{Style.RESET_ALL}")
