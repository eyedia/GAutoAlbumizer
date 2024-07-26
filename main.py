import os, sys, inspect
import argparse
import importlib
import configparser
import shutil

from common.gaa_config_parser import gaa_config_parser
from meta.metaFile import metaFileHandler
from exif.updateExif import exifHandler
from upload.GooglePhotoUploader import GooglePhotoUploader


# def getConfig(env="prod"):
#     if os.environ.get('EYEDIA_TECH_ENV') == "dev_local":
#         #print("Working in development environment.")
#         env = "dev_local"

#     configParser = configparser.ConfigParser()
#     full_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config.ini')
#     configParser.read(full_path)
#     if configParser.has_section(env):
#         config_section = configParser[env]
#         return galbumizer_config(config_section)
#     else:
#         raise ValueError(f'config {env} not found! Please update config.ini file and try again.')

# def resource_path(relative_path):
#     if hasattr(sys, '_MEIPASS'):
#         return os.path.join(sys._MEIPASS, relative_path)
#     return os.path.join(os.path.abspath("."), relative_path)

# def ensureEnvironment(config):
#     if not os.path.exists(config.getConfig("meta_album_dir")):
#         os.makedirs(config.getConfig("meta_album_dir"))

#     if not os.path.exists(config.getConfig("log_dir")):
#         os.makedirs(config.getConfig("log_dir"))
    
#     if config.getConfig("local") == "false" and not os.path.exists("sample_albums") and os.path.exists(resource_path(config.getConfig("sample_album_dir"))):
#         print("extracing sample albums...")
#         shutil.copytree(resource_path(config.getConfig("sample_album_dir")), "./sample_albums")

def main():

    config = gaa_config_parser(os.path.abspath(os.path.dirname(__file__)))
    if config is None:
        sys.exit(100)
    
    #ensureEnvironment(config)
    parser = argparse.ArgumentParser()
    parser.add_argument('--job', nargs='*', required=True)
    parser.add_argument('--input-dir', metavar='input_dir',dest='input_dir')
    parser.add_argument('--root-dir', metavar='root_dir',dest='root_dir')
    args = parser.parse_args()
    
    if len(args.job) == 0:
        parser.print_help()
        parser.exit()

    if args.job[0] == "scan":        
        if args.input_dir is not None:           
            metaFile = metaFileHandler(config)
            result = metaFile.parse_directory(args.input_dir, args.root_dir)
            print(f"Found {result[1]} files by scanning {result[0]} directories and {result[2]} albums identified.")

    elif args.job[0] == "exif":        
        exif = exifHandler(config)
        exif.updateExifs(config.getConfig("meta_album_dir"))

    elif args.job[0] == "show":
        print("Not implemented")
        metaFile = metaFileHandler()
        metaFile.split_csv(".\\data\\album_data.csv", ".\\data\\albums\\")
    
    elif args.job[0] == "upload":        
        uploader = GooglePhotoUploader(config)
        uploader.uploadAll()

    else:
        print("usage:")
        print("Scan folder          : --job scan --input-dir <input dir>")
        print("Update exif          : --job exif")
        print("Show Meta data       : --job show")
        print("Upload               : --job upload")


if __name__ == '__main__':
    main()
