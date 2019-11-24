#!/usr/bin/env python3

import os
import time
import zipfile
import sys



homedir = os.getenv('HOME')
name = 'work_backup_'+time.strftime('%d%m%Y')+'.zip'  # archive name
id_archive = os.popen("gdrive list | grep work | awk '{print$1}'").read().strip()

def backup():
    print('creating archive...')
    z = zipfile.ZipFile(name, 'w')
    print('backup homedir...')
    for root, dirs, files in os.walk(os.getenv('HOME')):
        for file in files:
            if name in files:
               files.remove(name)
            if '.vim' in dirs:
                dirs.remove('.vim')
            if '.git' in dirs:
                dirs.remove('.git')
            z.write(os.path.join(root, file))
    z.close()

def upload(archive):
    print('delete last cloud archive')
    os.system('gdrive delete ' + id_archive)
    print('upload archive...')
    os.system('gdrive upload ' + archive)
    print('delete local archive')
    os.remove(archive)
    print('\033[92mDONE!\033[92m')

def download():
    print('download archive...')
    os.system("gdrive download " + id_archive)
    return os.popen("gdrive list | grep work | awk '{print$2}'").read().strip()

def extract(archive):
    z = zipfile.ZipFile(archive, 'r')
    print('extract archive...')
    z.extractall('/')
    z.close()
    print('delete downloaded archive')
    os.remove(archive)

if sys.argv[1] == '-b':
    backup()
    upload(name)
elif sys.argv[1] == '-r':
    extract(download())
