import requests
from bs4 import BeautifulSoup
from bs4 import ResultSet, element


headers : dict = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive'
}

def GetCarPageInfo(carId : int, baseUrl: str = "https://www.shopcar.com.br/fichatecnica.php?id=") -> BeautifulSoup:
    
    url : str = f"{baseUrl}{carId}"
    print(f"Making a https request...")
    response : requests.Response = requests.get(url, headers=headers)

    statusCode : int = response.status_code
    if not response.ok:
        raise Exception(f"status code: {statusCode}. Reason: {response.reason}")
    else:
        print(f"request to {url} returned status code {statusCode}")

    return BeautifulSoup(response.content, 'html.parser')

def GetCarName(soup : BeautifulSoup) -> str:
    divCarName : ResultSet[element.Tag] =  soup.find_all("div", {"class": "img-principal"})
    for divCar in divCarName:
        spanText : element.Tag
        for spanText in divCar.find_all('span'):
            carName : str = spanText.text.strip() 
            print(f"Car name: {carName}")
            return carName

def GetCarInfoTable(soup : BeautifulSoup, carInfo2Extract : list[str] = ["l2 motor", "l2 d desempenho-rodas"]) -> dict[str, str]:
    dictToBeUpload  : dict = {}
    for carInfo in carInfo2Extract:
        liCarTable : ResultSet[element.Tag] = soup.find_all("li", {"class": carInfo})
        for div in liCarTable:
            # Within each div, find the first table element, if it exists.
            table : element.Tag = div.find('table')

            row : element.Tag
            for row in table.find_all('tr'):
                columns = row.find_all('td')
                text : str = ""

                # build a table to diplay the results - it's only for debug and understand the problem.
                if len(columns) == 1:
                    # print(f"\n{columns[0].text.strip():>40}")
                    continue
                else: 
                    for column in columns:
                        text += column.text.strip() + "-"
                    rowCells = text.split("-")
                    row = f"| {rowCells[0]:<30} | {rowCells[1]:<30} |"
                    dictToBeUpload[rowCells[0]] =  rowCells[1]
                    # print(row)
    return dictToBeUpload

def GetCarMeanPrice(soup : BeautifulSoup) -> float:
    liCarPrice : ResultSet[element.Tag] = soup.find_all("li", {"class": "tabela"})
    li : element.Tag
    for li in liCarPrice:
        ul : element.Tag = li.find("ul")
        meanPrice : float = 0.
        try:
            for li in ul:
                # print(li.text)
                if "Maior" in li.text  or "Menor" in li.text:
                        formatingPrice : str = li.text.replace("\xa0", " ").split("R$ ")[1]
                        formatingPrice = formatingPrice.replace(".", "").replace(",", ".")
                        meanPrice += float(formatingPrice)
            return meanPrice / 2
        except:
            print("It was not possible to calculate the mean price of the car.")
            return -999