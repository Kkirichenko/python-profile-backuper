#!/usr/bin/env python3
import os
import time
import sys

# colors
OKGREEN = '\033[92m'
FAILRED = '\033[91m'

# bash 
def bash(command):
    return os.popen(command).read().strip()

# source
wsl_user = bash('whoami')
homedir = bash('echo ~')
win_user = bash('cmd.exe /c "echo %USERNAME%" 2>/dev/null')
conemu = '/mnt/c/Users/'+win_user+'/AppData/Roaming/ConEmu.xml'
name = 'portablework_'+time.strftime('%d%m%Y')+'.tar.gz'

# restore
# ???


# backup
if len(sys.argv) < 2:
    source = conemu, homedir
    source = ' '.join(source)
elif sys.argv[1] == '--restore':
    cmd = "gdrive download `gdrive list | grep portablework | cut -f1 -d' ' | head -n1`"
    os.system(cmd)
    sys.exit()
elif sys.argv[1] == '--profile':
    source = homedir
elif sys.argv[1] == '--conemu':
    source = conemu
cmd = "sudo tar --exclude='/home/kkirichenko/windows_downloads' -zcf /home/{0} {1} 2>/dev/null && gdrive upload /home/{0} && sudo rm /home/{0}".format(name, source)
if os.system(cmd) == 0:
    print(OKGREEN + 'DONE' + OKGREEN)
else:
    print(FAILRED + 'FAILED' + FAILRED)
