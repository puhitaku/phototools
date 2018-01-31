#!/usr/bin/env python3

import os, shutil
from glob import glob
from datetime import datetime
from pathlib import Path

import piexif
from piexif import ImageIFD, ExifIFD


def join_paths(*dir_or_file):
    p = os.path.abspath('.')
    for d in dir_or_file:
        p = os.path.join(p, d)
    return p


def ensure_dir(dirname):
    if not Path(dirname).exists():
        os.mkdir(dirname)
    elif not Path(dirname).is_dir():
        raise Exception(f'Failed to make directory "{dirname}"')

ensure_dir('renamed')
ensure_dir('renamed_raw')
ensure_dir('renamed_vid')

pics = glob('**/DSC*.JPG', recursive=True)
pics += glob('**/DSC*.jpg', recursive=True)
pics += glob('**/DSC*.NEF', recursive=True)

for i, pic in enumerate(pics):
    print(f'{i} / {len(pics)}')

    exif = piexif.load(pic)
    date1 = exif['0th'][ImageIFD.DateTime].decode()
    date2 = exif['Exif'].get(ExifIFD.DateTimeOriginal, None).decode()
    
    if date2 is not None and date1 != date2:
        exif_date = date2
    else:
        exif_date = date1

    dt = datetime.strptime(exif_date, '%Y:%m:%d %H:%M:%S')
    fn_date = dt.strftime('%Y-%m-%d %H.%M.%S')

    if pic.lower().endswith('jpg'):
        folder, ex = 'renamed', 'jpg'
    elif pic.lower().endswith('nef'):
        folder, ex = 'renamed_raw', 'nef'

    count = 0
    dst = join_paths(folder, f'{fn_date}.{ex}')
    while os.path.isfile(dst):
        count += 1
        dst = join_paths(folder, f'{fn_date}_{count}.{ex}')

    shutil.move(pic, dst)

vids = glob('**/DSC*.MOV', recursive=True)
for i, vid in enumerate(vids):
    print(f'{i} / {len(vids)}')
    shutil.move(vid, join_paths('renamed_vid', Path(vid).name))

