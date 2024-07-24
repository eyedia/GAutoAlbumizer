import os, sys, inspect
import argparse
import importlib
import configparser

from meta.metaFile import metaFileHandler
from exif.updateExif import exifHandler


parser = argparse.ArgumentParser()
parser.add_argument('--job', nargs='*', required=True)
parser.add_argument('--job-args', nargs='*')
args = parser.parse_args()

if args.job[0] == "scan":
    dir_path = args.job_args[0]
    metaFile = metaFileHandler()
    metaFile.parse_directory(dir_path)

elif args.job[0] == "exif":
    file_path = ".\\data\\album_data.csv"
    exif = exifHandler()
    exif.updateExif(file_path)
else:
    print("usage:")
    print("Scan folder          : --job scan --job-args <input dir>")
    print("Update exif          : --job exif")
    print("Show Meta data       : --job show")
    print("Upload               : --job upload")
