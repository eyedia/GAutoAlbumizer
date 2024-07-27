import os, sys
import argparse
import pathlib

from common.gaa_config_parser import gaa_config_parser
from meta.metaFileHandler import metaFileHandler
from exif.ExifHandler import exifHandler
from upload.GooglePhotoUploader import GooglePhotoUploader


def main():

    config = gaa_config_parser(os.path.abspath(os.path.dirname(__file__)))
    if config is None:
        sys.exit(100)
    
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
        exif.updateExifs()

    elif args.job[0] == "show":
        print("Not implemented")
        print(os.path.join(pathlib.Path(os.getenv('LOCALAPPDATA')), "GAutoAlbumizer"))
    
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
