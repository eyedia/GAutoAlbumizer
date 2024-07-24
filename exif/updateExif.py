import pandas as pd 
import piexif
import datetime


class exifHandler:
    def __init__(self):
        self.name = 'self'       

    def updateExif(self, file_path):
        df = pd.read_csv(file_path, header=None, parse_dates = [2])        
        df = df.reset_index()  # make sure indexes pair with number of rows

        #print(df.info(verbose=True))
        total_columns = len(df.axes[1])
        for index, row in df.iterrows():
            if row[total_columns-2] == True:
                self.updateDateTime(row[total_columns-4], row[total_columns-3])


    def updateDateTime(self, fileName, dtTm):        
        createdDate = dtTm.strftime("%Y:%m:%d %H:%M:%S")
        exif_dict = piexif.load(fileName)    
        exif_dict['0th'][piexif.ImageIFD.DateTime] = createdDate
        exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = createdDate
        exif_dict['Exif'][piexif.ExifIFD.DateTimeDigitized] = createdDate
        exif_bytes = piexif.dump(exif_dict)
        piexif.insert(exif_bytes, fileName)
    