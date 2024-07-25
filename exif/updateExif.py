import pandas as pd 
import piexif
import datetime
from pathlib import Path
import warnings


class exifHandler:
    def __init__(self, config):
        self.name = 'self'
        self.config = config
        warnings.filterwarnings("error")  


    def updateExifs(self, input_dir):
        for p in Path(input_dir).glob('*.csv'):
            file_name = "{0}\\{1}".format(input_dir, p.name)
            self.updateExif(file_name)

    def updateExif(self, file_name):

        df = None
        try:
            df = pd.read_csv(file_name, header=None, parse_dates = [2], date_format='ISO8601')        
            df = df.reset_index()
        except UserWarning:
            print("The meta file was consistent data, most probably with the date column. Most common changes are when the CSV file is updated using Microsoft Excel and the dates are stripped off! Trying regenerating meta file by running scan command")
            return

        #print(df.info(verbose=True))
        #total_columns = len(df.axes[1])
        for index, row in df.iterrows():
            if row[3] == True:
                self.updateDateTime(row[1], row[2])


    def updateDateTime(self, fileName, dtTm):
        print(f"updating Exif: {fileName}", end= " ")
        if not isinstance(dtTm, pd.Timestamp):
            print(f"{dtTm} is not valid! Cannot update!")
            return
             
        createdDate = dtTm.strftime("%Y:%m:%d %H:%M:%S")
        exif_dict = piexif.load(fileName)    
        exif_dict['0th'][piexif.ImageIFD.DateTime] = createdDate
        exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = createdDate
        exif_dict['Exif'][piexif.ExifIFD.DateTimeDigitized] = createdDate
        exif_bytes = piexif.dump(exif_dict)
        piexif.insert(exif_bytes, fileName)
        print("Done!")
    