from bs4 import BeautifulSoup
from Model import DataShopCarInfo
from bs4 import ResultSet, element
from ShopCar.ShopCarRequest import GetCarPageInfo, GetCarName, GetCarInfoTable, GetCarMeanPrice


def GenerateData(carId : int) -> None:
    soup: BeautifulSoup = GetCarPageInfo(carId)

    carModel = DataShopCarInfo.ShopCarInfo("unknown", -999., {})
    # Get car name
    carModel.carName = GetCarName(soup)

    # Get some specs of the car
    carInfo2Extract : list[str] = ["l2 motor", "l2 d desempenho-rodas"]
    carModel.tableInfo.update(GetCarInfoTable(soup, carInfo2Extract))

    # Get car price
    carModel.price = GetCarMeanPrice(soup)

    carModel.GenerateCsvData()


def ExtractData(consecutiveTries : int = 25, maxIdValue : int = 500) -> None:
    print(f"Initializing extraction of cars infos.")
    print(f"Upper limit of car id: {maxIdValue}")
    print(f"Max of consucutevies retries with error: {consecutiveTries}")

    currentCarId : int = 0
    retryNumber : int = 0
    while (currentCarId <= maxIdValue and retryNumber < 25):

        try:
            print(f"Getting info from car id {currentCarId}")
            GenerateData(currentCarId)

            currentCarId += 1
            retryNumber = 0

        except Exception as e:
            retryNumber += 1
            currentCarId += 1
            print(f"An error occurred: Reason: {str(e)}\nError counter {retryNumber}")
            continue

    print("Info extraction ended.")