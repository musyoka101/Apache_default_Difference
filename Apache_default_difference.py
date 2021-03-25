#!/usr/bin/env python3

import requests
import io
from cmd import Cmd
import os
import sys
import re

requests.packages.urllib3.disable_warnings()

class bcolors:
        OKBLUE = '\033[94m'
        OKGREEN = '\033[92m'
        FAIL = '\033[91m'
        LIGHTGREY='\033[37m'
        WARNING = '\033[93m'
        ORANGE='\033[33m'
        ENDC = '\033[0m'

class Terminal(Cmd):
    intro = f"{bcolors.ORANGE}[+] Apache2 Diff\n[+]Finding what's different from the Apache default pages\n[+]Author: Musyoka Ian{bcolors.ENDC}"
    prompt = f"{bcolors.WARNING}\n[+] Enter the URL: {bcolors.ENDC}"
    def default(self,args):
        searcher(args)

def searcher(url):
    current_directory = os.getcwd()
    connection = requests.get(url, verify=False).text
    print (f"{bcolors.OKGREEN}[+] Trying to identify the operating system the server is using{bcolors.ENDC}")
    operating_system = re.search("\x70\x61\x63\x68\x65\x32\x20(.*?)\x44\x65\x66\x61\x75\x6c", connection).group(1)
    print (f"[+] The Target seems to be running: {bcolors.FAIL}{operating_system}{bcolors.ENDC}")
    print (f"{bcolors.OKGREEN}[+] Reading the default {operating_system.strip()} Apache2 index page from {current_directory}/{operating_system.strip()}.index.html{bcolors.ENDC}")
    content = open(f"{operating_system.strip()}.index.html").readlines()
    buffered = io.StringIO(connection)
    buffered = buffered.readlines()
    difference = []
    for line in buffered:
        if line not in content:
            difference.append(line)
    if not difference:
        print(f"{bcolors.FAIL}[-] They are identical{bcolors.ENDC}")
    else:
        print()
        for result in difference:
            if not result:
                pass
            else:
                print(f"{bcolors.LIGHTGREY}+  {result.strip()}{bcolors.ENDC}")
    print (f"{bcolors.OKBLUE}[-] Exiting!!!!!!{bcolors.ENDC}")
    sys.exit(1)
if __name__ == ("__main__"):
    terminal = Terminal()
    terminal.cmdloop()
