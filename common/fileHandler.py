import os
import pandas as pd 
from pathlib import Path

class FileHandler:

    def __init__(self):
        self.name = 'self'

    def split_csv(self, csvFilePath, newDirPath):
        df = pd.read_csv(csvFilePath)
        for (n), group in df.groupby(df.columns[0]):
            group.to_csv(f'{newDirPath}{n}_xxtempxx.csv')

        self.remove_first_column(newDirPath)

    def sort_csv(self, fromFileName, toFileName, deleteFromFile=True):
        pd.read_csv(fromFileName, header=None).sort_values([0,1], ascending=[True, False]).to_csv(toFileName, index=False, header=None)

        if deleteFromFile:
            os.remove(toFileName)

    def remove_first_column(self, dir_path):

        temp_files = []
        for p in Path(dir_path).glob('*_xxtempxx.csv'):
            file_name = "{0}\\{1}".format(dir_path, p.name)            
            temp_files.append(file_name)
            df = pd.read_csv(file_name, header=None)
            df = df.drop(df.columns[0], axis=1)
            df.to_csv(file_name.replace("_xxtempxx", ""), index=False, header=None)

        
        for temp_file in temp_files:
            os.remove(temp_file)
            