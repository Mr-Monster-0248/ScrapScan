import requests
import shutil

def searchScan(myURL) -> (str, str):
    """
    Fuction that search for scan acording to an input by the user

    -----
    Return tables of choices names and choices url code
    """
    search = input("Scan to find: ")
    searchURL = myURL + "search?query=" + search
    print("quering", searchURL)
    resp = requests.get(searchURL)

    choiceURL = []
    choiceName = []
    if(resp.status_code == 200):
        data = resp.json()
        for item in data:
            for i in data[item]:
                choiceName.append(i['value'])
                choiceURL.append(i['data'])
    else:
        print("Error request:" , resp.status_code)

    del resp
    return choiceName, choiceURL

def userChoice(choiceName):
    print("Choose the manga you want in this list")
    for i in range(len(choiceName)):
        print(i, "->", choiceName[i])
    
    choice = -1
    while(choice < 0 or choice > len(choiceName)):
        choice = int(input("Your choice: "))

    return choice

if __name__ == "__main__":
    myURL = "https://www.scan-vf.co/"

    choiceName, choiceURL = searchScan(myURL)
    userChoice(choiceName)
