import os, sys, inspect
import argparse
import importlib
import configparser

from common.config import galbumizer_config
from meta.metaFile import metaFileHandler
from exif.updateExif import exifHandler
from upload.GooglePhotoUploader import GooglePhotoUploader


def getConfig(env="dev_local"):    
    configParser = configparser.ConfigParser()
    full_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config.ini')
    configParser.read(full_path)
    if configParser.has_section(env):
        config_section = configParser[env]
        return galbumizer_config(config_section)
    else:
        raise ValueError(f'config {env} not found! Please update config.ini file and try again.')

def main():
    config = getConfig()
    if config is None:
        sys.exit(100)
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--job', nargs='*', required=True)
    parser.add_argument('--input-dir', metavar='input_dir',dest='input_dir')
    args = parser.parse_args()
    
    if len(args.job) == 0:
        parser.print_help()
        parser.exit()

    if args.job[0] == "scan":        
        if args.input_dir is not None:           
            metaFile = metaFileHandler(config)
            metaFile.parse_directory(args.input_dir)

    elif args.job[0] == "exif":        
        exif = exifHandler(config)
        exif.updateExifs(config.getConfig("meta_album_dir"))

    elif args.job[0] == "show":
        print("Not implemented")
        metaFile = metaFileHandler()
        metaFile.split_csv(".\\data\\album_data.csv", ".\\data\\albums\\")
    
    elif args.job[0] == "upload":
        albumName = args.job_args[0]
        photos = args.job_args[1]
        uploader = GooglePhotoUploader()
        uploader.upload(albumName, photos)

    else:
        print("usage:")
        print("Scan folder          : --job scan --input-dir <input dir>")
        print("Update exif          : --job exif")
        print("Show Meta data       : --job show")
        print("Upload               : --job upload")


if __name__ == '__main__':
    main()
