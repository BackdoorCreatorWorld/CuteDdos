#!/data/data/com.termux/files/usr/bin/python3
# -*- coding: utf-8 -*-

"""
ARCHITECT 01 - DDoS Attack Suite
Professional Attack Framework
Main Entry Point with Password Protection
"""

import os
import sys
import time
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def clear_screen():
    """Clear terminal screen"""
    os.system('clear' if os.name == 'posix' else 'cls')

def print_auth_banner():
    """Print authentication banner - DDOS BESAR, sisanya kecil"""
    banner = f"""
{Fore.RED}
██████╗ ██████╗  ██████╗ ███████╗
██╔══██╗██╔══██╗██╔═══██╗██╔════╝
██║  ██║██║  ██║██║   ██║███████╗
██║  ██║██║  ██║██║   ██║╚════██║
██████╔╝██████╔╝╚██████╔╝███████║
╚═════╝ ╚═════╝  ╚═════╝ ╚══════╝
{Style.RESET_ALL}
{Fore.CYAN}═══════════════════════════════════════════{Style.RESET_ALL}
{Fore.GREEN}ARCHITECT 01 - PROFESSIONAL ATTACK SUITE v2.0{Style.RESET_ALL}
{Fore.YELLOW}═══════════════════════════════════════════{Style.RESET_ALL}

{Fore.RED}⚠️  AUTHENTICATION REQUIRED  ⚠️{Style.RESET_ALL}
    """
    print(banner)

def authenticate():
    """Authenticate user with password"""
    attempts = 3
    
    while attempts > 0:
        print(f"{Fore.CYAN}╭─❯ Enter access password{Style.RESET_ALL}")
        password = input(f"{Fore.CYAN}╰─❯ {Style.RESET_ALL}").strip()
        
        # Simple string comparison
        if password in ["CuteDdos", "NanoHas", "FBI", "Brick"]:
            print(f"{Fore.GREEN}\n╰─❯ Access granted! Loading suite...{Style.RESET_ALL}")
            time.sleep(1)
            return True
        else:
            attempts -= 1
            if attempts > 0:
                print(f"{Fore.RED}╰─❯ Access denied! {attempts} attempts remaining.{Style.RESET_ALL}\n")
            else:
                print(f"{Fore.RED}╰─❯ Too many failed attempts. Exiting...{Style.RESET_ALL}")
                time.sleep(2)
                return False
    
    return False

def loading_animation():
    """Show loading animation"""
    print(f"{Fore.YELLOW}")
    for i in range(3):
        print(f"╰─❯ Loading" + "." * (i + 1))
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
        print(f"{Fore.RED}╰─❯ Error loading modules: {e}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}╰─❯ Make sure you're in the correct directory{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}╰─❯ Structure should be:{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}    ddos-attack-suite/{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}    ├── main.py{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}    └── core/{Style.RESET_ALL}")
        time.sleep(5)
    except KeyboardInterrupt:
        print(f"{Fore.RED}\n╰─❯ Interrupted. Exiting...{Style.RESET_ALL}")
        sys.exit(0)

if __name__ == "__main__":
    main()
