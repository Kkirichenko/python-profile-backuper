#!/usr/bin/env python3
import os
import re
import time
import sys
import zipfile

# bash 
def bash(command):
    return os.popen(command).read().strip()

# colors
OK_GREEN = '\033[92m'
FAIL_RED = '\033[91m'

# source
wsl_user = bash('whoami') # wsl linux user
win_user = bash('cmd.exe /c "echo %USERNAME%" 2>/dev/null') # windows user 
homedir = bash('echo ~') # wsl home dir
conemu = '/mnt/c/Users/'+win_user+'/AppData/Roaming/ConEmu.xml' # CenEmu config 
name = 'portablework_'+time.strftime('%d%m%Y')+'.zip' # archive name
script_path = os.path.dirname(os.path.realpath(__file__))

# backup
def backup():
    z = zipfile.ZipFile(name, 'w')
    for root, dirs, files in os.walk(homedir):
        for file in files:
            if os.path.basename(os.path.dirname(os.path.realpath(__file__))) in dirs:
                dirs.remove(os.path.basename(os.path.dirname(os.path.realpath(__file__))))
            z.write(os.path.join(root, file))
    z.write(conemu)
    z.write('/etc/vim/vimrc')
    z.close()
    print(OK_GREEN+"Backup DONE!"+OK_GREEN)

def upload():
    print("UPLOAD TO GDRIVE "+name)
    os.system('gdrive upload '+name) 
    print("OK!")
    os.system('rm '+name)
    print(name+' DELETED!')
backup()
upload()
# restore
#z = zipfile.ZipFile(name, 'r')
#z.extractall('/')

# restore
#z.extractall(sys.argv[1])

# backup
#if len(sys.argv) < 2:
#    source = conemu, homedir
#    source = ' '.join(source)
#elif sys.argv[1] == '--restore':
#    cmd = "gdrive download `gdrive list | grep portablework | cut -f1 -d' ' | head -n1`"
#    os.system(cmd)
#    sys.exit()
#elif sys.argv[1] == '--profile':
#    source = homedir
#elif sys.argv[1] == '--conemu':
#    source = conemu
#cmd = "sudo tar --exclude='/home/kkirichenko/windows_downloads' -zcf /home/{0} {1} 2>/dev/null && gdrive upload /home/{0} && sudo rm /home/{0}".format(name, source)
#if os.system(cmd) == 0:
#    print(OKGREEN + 'DONE' + OKGREEN)
#else:
#    print(FAILRED + 'FAILED' + FAILRED)
