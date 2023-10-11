import dataclasses
import csv
from os.path import join, exists
from os import makedirs

def VerifyIfDirExists(folderPath):
    if not exists(folderPath):
        print(f"Directory {folderPath} does not exist. Creating...")
        makedirs(folderPath)
                
@dataclasses.dataclass
class ShopCarInfo:
    """Class to store car info from shopcar.com.br table"""
    carName: str
    price: float
    tableInfo: dict = dataclasses.field(default_factory=dict)


    def addTableInfo(self, key, value) -> None: 
        self.tableInfo.update({key: value})
    
    
    def GenerateCsvData(self, folderPath : str = "TempCsv/"):
        # Remove empty space
        VerifyIfDirExists(folderPath)
        csvFileName : str = f"{self.carName.replace(' ','').replace('/', '_')}.csv"
        csvFileName = join(folderPath, csvFileName)
        print(f"The .csv file {csvFileName} was created!")
        with open(csvFileName, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=self.tableInfo.keys())
            writer.writeheader()

            # Write the data rows
            for row in [self.tableInfo]:
                writer.writerow(row)
