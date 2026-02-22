#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
URL Validator for DDoS Attacks
Architect 01 - Professional Suite
SUPPORT ALL URL TYPES
"""

import re
from urllib.parse import urlparse

def validate_url(url):
    """
    Validate URL format - Support semua jenis
    """
    if not url:
        return False, None, "URL cannot be empty"
    
    url = url.strip()
    
    if not url.startswith(('http://', 'https://', 'ftp://')):
        ip_pattern = r'^(\d{1,3}\.){3}\d{1,3}(:\d+)?$'
        if re.match(ip_pattern, url.split('/')[0]):
            url = 'http://' + url
        elif url.startswith('localhost') or url.startswith('127.0.0.1'):
            url = 'http://' + url
        elif '.' in url.split('/')[0]:
            url = 'http://' + url
        else:
            url = 'http://' + url
    
    try:
        parsed = urlparse(url)
        
        if not parsed.netloc and not parsed.path:
            return False, None, "Invalid URL format"
        
        if not parsed.netloc and parsed.path:
            return False, None, "Relative URL not allowed. Use full URL with domain/IP"
        
        if parsed.netloc:
            host = parsed.netloc.split(':')[0]
            ip_parts = host.split('.')
            if len(ip_parts) == 4 and all(part.isdigit() for part in ip_parts):
                for part in ip_parts:
                    if int(part) > 255:
                        return False, None, "Invalid IP address (octet > 255)"
        
        return True, url, None
        
    except Exception as e:
        return False, None, f"URL validation error: {str(e)}"

def get_target_url():
    """
    Prompt user for URL and validate until valid
    """
    from colorama import Fore, Style
    
    print(Fore.YELLOW + "\n╰─❯ Supported formats:" + Style.RESET_ALL)
    print(Fore.YELLOW + "    • http://example.com" + Style.RESET_ALL)
    print(Fore.YELLOW + "    • https://example.com" + Style.RESET_ALL)
    print(Fore.YELLOW + "    • example.com (auto-add http)" + Style.RESET_ALL)
    print(Fore.YELLOW + "    • 192.168.1.1 (auto-add http)" + Style.RESET_ALL)
    print(Fore.YELLOW + "    • localhost:8080 (auto-add http)" + Style.RESET_ALL)
    print(Fore.YELLOW + "    • ftp://example.com" + Style.RESET_ALL)
    print(Fore.YELLOW + "    • site.com/path?query=1 (auto-add http)" + Style.RESET_ALL)
    
    while True:
        print(f"\n{Fore.CYAN}╭─❯ Enter target URL for this attack{Style.RESET_ALL}")
        url = input(f"{Fore.CYAN}╰─❯ {Style.RESET_ALL}").strip()
        
        is_valid, formatted_url, error = validate_url(url)
        
        if is_valid:
            print(f"{Fore.GREEN}╰─❯ URL valid: {formatted_url}{Style.RESET_ALL}\n")
            return formatted_url
        else:
            print(f"{Fore.RED}╰─❯ Error: {error}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}╰─❯ Please enter a valid URL{Style.RESET_ALL}")
