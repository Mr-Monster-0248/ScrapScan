import requests
import shutil


def searchScan(my_url) -> (str, str):
    """
    Fuction that search for scan acording to an input by the user

    -----
    Return tables of choices names and choices url code
    """
    search = input("Scan to find: ")
    searchURL = my_url + "search?query=" + search
    print("quering", searchURL)
    resp = requests.get(searchURL)

    choice_url = []
    choice_name = []
    if resp.status_code == 200:
        data = resp.json()
        for item in data:
            for i in data[item]:
                choice_name.append(i['value'])
                choice_url.append(i['data'])
    else:
        print("Error request:", resp.status_code)

    del resp
    return choice_name, choice_url


def userChoice(choice_name):
    print("Choose the manga you want in this list")
    for i in range(len(choice_name)):
        print(i, "->", choice_name[i])

    choice = -1
    while choice < 0 or choice > len(choice_name):
        choice = int(input("Your choice: "))

    return choice


if __name__ == "__main__":
    myURL = "https://www.scan-vf.co/"

    choiceName, choiceURL = searchScan(myURL)
    userChoice(choiceName)
