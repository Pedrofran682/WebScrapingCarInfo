import dataclasses
import csv
from os.path import join


@dataclasses.dataclass
class ShopCarInfo:
    """Class to store car info from shopcar.com.br table"""
    carName: str
    price: float
    tableInfo: dict = dataclasses.field(default_factory=dict)


    def addTableInfo(self, key, value) -> None: 
        self.tableInfo.update({key: value})
    
    
    def GenerateCsvData(self, folderPath : str = "TempCsv"):
        # Remove empty space
        csvFileName : str = f"{self.carName.replace(' ','')}.csv"
        csvFileName = join(folderPath, csvFileName)

        with open(csvFileName, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=self.tableInfo.keys())
            writer.writeheader()

            # Write the data rows
            for row in [self.tableInfo]:
                writer.writerow(row)



