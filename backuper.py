#!/usr/bin/env python3
import os
import re
import time
import sys
import zipfile


# bash
def bash(command):
    return os.popen(command).read().strip()

# warn colors
OK_GREEN = '\033[92m'
FAIL_RED = '\033[91m'

# variables
script_path = os.path.dirname(os.path.realpath(__file__))
name = 'portablework_'+time.strftime('%d%m%Y')+'.zip'  # archive name
wsl_user = bash('whoami')  # wsl linux user
win_user = bash('cmd.exe /c "echo %USERNAME%" 2>/dev/null')  # windows user
# source
homedir = bash('echo ~')  # wsl home dir
conemu = '/mnt/c/Users/'+win_user+'/AppData/Roaming/ConEmu.xml'  # CenEmu conf
vimrc = '/etc/vim/vimrc'
sshconf = '/etc/ssh/ssh_config'
# files source list
f_source = [conemu, vimrc, sshconf]


# backup
def backup():
    # open archive
    print('creating archive...')
    z = zipfile.ZipFile(name, 'w')
# backup homedir
    for root, dirs, files in os.walk(homedir):
        for file in files:
            if os.path.basename(os.path.dirname(os.path.realpath(__file__))) in dirs:
                dirs.remove(os.path.basename(os.path.dirname(os.path.realpath(__file__))))
            z.write(os.path.join(root, file))
# backup other stuff
    for file in f_source:
        z.write(file)
    z.close()


def upload():
    os.system('gdrive upload '+name)
    os.system('rm '+name)

backup()
upload()
print(OK_GREEN+'DONE!'+OK_GREEN)

