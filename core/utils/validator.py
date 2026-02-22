#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
URL Validator for DDoS Attacks
Architect 01 - Professional Suite
"""

import re
from urllib.parse import urlparse

def validate_url(url):
    """
    Validate URL format and accessibility
    
    Returns:
        tuple: (is_valid, formatted_url, error_message)
    """
    if not url:
        return False, None, "URL cannot be empty"
    
    # Add scheme if missing
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    
    # Parse URL
    try:
        parsed = urlparse(url)
        
        # Check basic structure
        if not parsed.netloc:
            return False, None, "Invalid URL format (missing domain)"
        
        # Check for valid domain characters
        domain_pattern = re.compile(
            r'^(?:[a-zA-Z0-9]'  # First character
            r'(?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)'  # Subdomain
            r'+[a-zA-Z]{2,}$'  # TLD
        )
        
        # Simple validation - at least have dots
        if '.' not in parsed.netloc:
            return False, None, "Domain must contain at least one dot (.)"
        
        # Check for IP address format (optional, but valid)
        ip_pattern = re.compile(r'^(\d{1,3}\.){3}\d{1,3}(:\d+)?$')
        if ip_pattern.match(parsed.netloc.split(':')[0]):
            # Validate IP octets
            octets = parsed.netloc.split(':')[0].split('.')
            for octet in octets:
                if int(octet) > 255:
                    return False, None, "Invalid IP address (octet > 255)"
        
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
    
    while True:
        url = input(f"{Fore.CYAN}   ╰─❯ Enter target URL: {Style.RESET_ALL}").strip()
        
        is_valid, formatted_url, error = validate_url(url)
        
        if is_valid:
            print(f"{Fore.GREEN}   ╰─❯ URL valid: {formatted_url}{Style.RESET_ALL}\n")
            return formatted_url
        else:
            print(f"{Fore.RED}   ╰─❯ Error: {error}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}   ╰─❯ Please enter a valid URL (e.g., https://example.com){Style.RESET_ALL}\n")
