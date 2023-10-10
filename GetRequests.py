import requests
from bs4 import BeautifulSoup
from Model import ShopCarInfo
from bs4 import ResultSet
from bs4 import element

headers : dict = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive'
}

url : str = "https://www.shopcar.com.br/fichatecnica.php?id=219"
response : requests.Response = requests.get(url, headers=headers)

statusCode : int = response.status_code
if not response.ok:
    raise Exception(f"status code: {statusCode}. Reason: {response.reason}")
else:
    print(f"request to {url} returned status code {statusCode}")

soup: BeautifulSoup = BeautifulSoup(response.content, 'html.parser')

# Get car name
divCarName : ResultSet[element.Tag] =  soup.find_all("div", {"class": "img-principal"})
for divCar in divCarName:
    spanText : element.Tag
    for spanText in divCar.find_all('span'):
        print(spanText.text.strip())

carInfo2Extract : list[str] = ["l2 motor", "l2 d desempenho-rodas"]
# Get some specs of the car
for carInfo in carInfo2Extract:
    liCarTable : ResultSet[element.Tag] = soup.find_all("li", {"class": carInfo})
    for div in liCarTable:
        # Within each div, find the first table element, if it exists
        table : element.Tag = div.find('table')

        row : element.Tag
        for row in table.find_all('tr'):
            columns = row.find_all('td')
            text : str = ""

            # build a table to diplay the results - it's only for debug and understand the problem
            if len(columns) == 1:
                print(f"\n{columns[0].text.strip():>40}")
            else: 
                for column in columns:
                    text += column.text.strip() + "-"
                rowCells = text.split("-")
                row = f"| {rowCells[0]:<30} | {rowCells[1]:<30} |"
                print(row)

# Get car price
liCarPrice : ResultSet[element.Tag] = soup.find_all("li", {"class": "tabela"})
li : element.Tag
for li in liCarPrice:
    ul : element.Tag = li.find("ul")
    for li in ul:
        print(li.text)