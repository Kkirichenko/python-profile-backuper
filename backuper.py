#!/usr/bin/env python3

import os
import time
import zipfile
import argparse


homedir = os.getenv('HOME')
name = 'work_backup_'+time.strftime('%d%m%Y')+'.zip'  # archive name
id_archive = os.popen(
    "gdrive list | grep work | awk '{print$1}'").read().strip()


def backup():
    print('creating archive', end=' ', flush='True')
    z = zipfile.ZipFile(name, 'w')
    print('✓')
    print('backup homedir',end=' ', flush='True')
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
    print('✓')


def upload(archive):
    print('delete last cloud archive')
    os.system('gdrive delete ' + id_archive)
    print('upload archive')
    os.system('gdrive upload ' + archive)
    print('delete local archive', end=' ', flush='True')
    os.remove(archive)
    print('✓')


def download():
    print('download archive', end=' ', flush='True')
    os.system("gdrive download " + id_archive)
    return os.popen("gdrive list | grep work | awk '{print$2}'").read().strip()
    print('✓')


def extract(archive):
    z = zipfile.ZipFile(archive, 'r')
    print('extract archive', end=' ', flush='True')
    z.extractall('/')
    z.close()
    print('✓')
    print('delete downloaded archive', end=' ', flush='True')
    os.remove(archive)
    print('✓')


parser = argparse.ArgumentParser(
    description='backup/restore homedir into/from google drive')
parser.add_argument('--backup', '-b', action='store_true', help='backup homedir to gdrive')
parser.add_argument('--restore', '-r', action='store_true', help='restore homedir from gdrive')
args = parser.parse_args()

if args.backup:
    backup()
    upload(name)
    print('\033[92mBACKUP DONE!\033[92m')
elif args.restore:
    extract(download())
    print('\033[92mRESTORE DONE!\033[92m')
