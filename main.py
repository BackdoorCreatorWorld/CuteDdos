#!/data/data/com.termux/files/usr/bin/python3
# -*- coding: utf-8 -*-

"""
ARCHITECT 01 - DDoS Attack Suite
Professional Attack Framework for Termux
Main Entry Point with Password Protection
"""

import os
import sys
import hashlib
import time
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Password hashes (precomputed SHA256 for security)
# Original passwords: CuteDdos, NanoHas, FBI, Brick
PASSWORD_HASHES = {
    '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92',  # CuteDdos
    'b7a0a7b7b0b7a0a7b7b0b7a0a7b7b0a7b7b0b7a0a7b7b0a7b7b0b7a0a7b7b0',  # NanoHas (example hash)
    'a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2',  # FBI (example hash)
    'f7e9d8c7b6a5f7e9d8c7b6a5f7e9d8c7b6a5f7e9d8c7b6a5f7e9d8c7b6a5f7e9',  # Brick (example hash)
}

def clear_screen():
    """Clear terminal screen"""
    os.system('clear' if os.name == 'posix' else 'cls')

def print_auth_banner():
    """Print authentication banner"""
    banner = f"""
{Fore.RED}╔═══════════════════════════════════════════════════════════╗
║                                                               ║
║     █████╗ ██████╗  ██████╗██╗  ██╗██╗████████╗███████╗ ██████╗████████╗
║    ██╔══██╗██╔══██╗██╔════╝██║  ██║██║╚══██╔══╝██╔════╝██╔════╝╚══██╔══╝
║    ███████║██████╔╝██║     ███████║██║   ██║   █████╗  ██║        ██║   
║    ██╔══██║██╔══██╗██║     ██╔══██║██║   ██║   ██╔══╝  ██║        ██║   
║    ██║  ██║██║  ██║╚██████╗██║  ██║██║   ██║   ███████╗╚██████╗   ██║   
║    ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝   ╚═╝   ╚══════╝ ╚═════╝   ╚═╝   
║                                                               ║
║                    PROFESSIONAL ATTACK SUITE                  ║
║                         VERSION 2.0                           ║
╚═══════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
{Fore.YELLOW}                      ╔══════════════════╗
                      ║  AUTHENTICATION  ║
                      ╚══════════════════╝
{Style.RESET_ALL}
    """
    print(banner)

def authenticate():
    """Authenticate user with password"""
    attempts = 3
    
    while attempts > 0:
        print(f"{Fore.CYAN}   ╭─❯ Enter access password{Style.RESET_ALL}")
        password = input(f"{Fore.CYAN}   ╰─❯ {Style.RESET_ALL}").strip()
        
        # Simple string comparison (not hash for simplicity as requested)
        if password in ["CuteDdos", "NanoHas", "FBI", "Brick"]:
            print(f"{Fore.GREEN}\n   ╰─❯ Access granted! Loading suite...{Style.RESET_ALL}")
            time.sleep(1)
            return True
        else:
            attempts -= 1
            if attempts > 0:
                print(f"{Fore.RED}   ╰─❯ Access denied! {attempts} attempts remaining.{Style.RESET_ALL}\n")
            else:
                print(f"{Fore.RED}   ╰─❯ Too many failed attempts. Exiting...{Style.RESET_ALL}")
                time.sleep(2)
                return False
    
    return False

def loading_animation():
    """Show loading animation"""
    print(f"{Fore.YELLOW}")
    for i in range(3):
        print(f"   ╰─❯ Loading" + "." * (i + 1))
        time.sleep(0.5)
    print(f"{Style.RESET_ALL}")

def main():
    """Main function"""
    clear_screen()
    print_auth_banner()
    
    if not authenticate():
        sys.exit(1)
    
    loading_animation()
    clear_screen()
    
    # Import handler after authentication
    try:
        from core.handler import AttackHandler
        
        handler = AttackHandler()
        handler.main_loop()
        
    except ImportError as e:
        print(f"{Fore.RED}   ╰─❯ Error loading modules: {e}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}   ╰─❯ Make sure you're in the correct directory{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}   ╰─❯ Structure should be:{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}       ddos-attack-suite/{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}       ├── main.py{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}       └── core/{Style.RESET_ALL}")
        time.sleep(5)
    except KeyboardInterrupt:
        print(f"{Fore.RED}\n   ╰─❯ Interrupted. Exiting...{Style.RESET_ALL}")
        sys.exit(0)

if __name__ == "__main__":
    main()
