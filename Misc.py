import os
import sys
import json
import errno
from colorama import Fore, Back, Style

def eprint(msg):
    print(Style.BRIGHT + Fore.RED + msg + Style.RESET_ALL, file=sys.stderr)

def wprint(msg):
    print(Style.BRIGHT + Fore.YELLOW + msg + Style.RESET_ALL)

def sprint(msg):
    print(Style.BRIGHT + Fore.GREEN + msg + Style.RESET_ALL)

def isFileExist(filename):
    if not os.path.isfile(filename): 
        eprint("No such file : " + filename)
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), filename)
    return True

def isModuleExist(filename):
    if os.path.isdir(filename):
        return filename
    else:
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), filename)