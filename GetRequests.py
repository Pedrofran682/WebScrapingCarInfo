from bs4 import BeautifulSoup
from Model import DataShopCarInfo
from bs4 import ResultSet, element
from ShopCar.ShopCarRequest import GetCarPageInfo, GetCarName, GetCarInfoTable, GetCarMeanPrice



soup: BeautifulSoup = GetCarPageInfo(219)

carModel = DataShopCarInfo.ShopCarInfo("unknown", -999., {})
# Get car name
carModel.carName = GetCarName(soup)

# Get some specs of the car
carInfo2Extract : list[str] = ["l2 motor", "l2 d desempenho-rodas"]
carModel.tableInfo.update(GetCarInfoTable(soup, carInfo2Extract))

# Get car price
carModel.price = GetCarMeanPrice(soup)

carModel.GenerateCsvData()