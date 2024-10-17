from shutil import get_terminal_size as gts
from colorama import Fore, Style
from time import sleep

andge_group = f'''


████████  ██████      ██   ██ ███████  █████  ████████ ██ ███    ██  ██████  
   ██    ██           ██   ██ ██      ██   ██    ██    ██ ████   ██ ██       
   ██    ██   ███     ███████ █████   ███████    ██    ██ ██ ██  ██ ██   ███ 
   ██    ██    ██     ██   ██ ██      ██   ██    ██    ██ ██  ██ ██ ██    ██ 
   ██     ██████      ██   ██ ███████ ██   ██    ██    ██ ██   ████  ██████  
                                                                             
                                                                             
'''


def banner():
    for andge in andge_group.split('\n'):
        print(Fore.YELLOW + andge.center(gts()[0], ' ') + Style.RESET_ALL)
        sleep(0.065)