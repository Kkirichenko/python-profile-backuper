#!/usr/bin/env python3
import os
import re
import time
import sys
import zipfile


# bash
def bash(cmd):
    return os.popen(cmd).read().strip()

# warn colors
OK_GREEN = '\033[92m'
FAIL_RED = '\033[91m'

# variables
script_path = os.path.dirname(os.path.realpath(__file__))
name = 'portablework_'+time.strftime('%d%m%Y')+'.zip'  # archive name
wsl_user = bash('whoami')  # wsl linux user
win_user = bash('cmd.exe /c "echo %USERNAME%" 2>/dev/null')  # windows user
# source
homedir = bash('echo ~')  # ws home dir
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
    print('backup homedir...')
# backup homedir
    for root, dirs, files in os.walk(homedir):
        for file in files:
            if name in files:
                files.remove(name)
            z.write(os.path.join(root, file))
# backup other stuff
    for file in f_source:
        z.write(file)
    print('backup some stuff')
    z.close()


# upload then delete archive
def upload(archive):
    print('uploading archive...')
    bash('gdrive upload '+archive)
    print('delete local archive')
    bash('rm '+archive)
    print(OK_GREEN+'DONE!'+OK_GREEN)


# download archive
def download():
    print('Download archive...')
    bash("gdrive download `gdrive list | grep work | sort -rk 2,2 | awk 'NR==1{print$1}'`") 
    return bash("gdrive list | grep work | sort -rk 2,2 | awk 'NR==1{print$2}'")


# exctract all from archive
def extract(archive):
    z = zipfile.ZipFile(archive, 'r')
    print('extract archive...')
    z.extractall('/')
    z.close()
    print('delete local archive')
    bash('rm '+archive)
    


# keys
if sys.argv[1] == '-b':
    backup()
    upload(name)
elif sys.argv[1] == '-r':
    extract(download())
