import scrap_scan_vf as ssvf
import scangetter

# the only url working for now
myURL = "https://www.scan-vf.co/"

choiceNames, choiceURL = scangetter.searchScan(myURL)
choice = scangetter.userChoice(choiceNames)

folderName = choiceNames[choice]
preformatURL = "https://www.scan-vf.co/uploads/manga/{}/chapters/"
scanVF_URL =  preformatURL.format(choiceURL[choice])

print("Scraping for", folderName)

try:
    chapNumber = int(input("Chapter to start(0 default): "))
except:
    chapNumber = 0

print("Stop with ctrl+c")
ssvf.scrapScan_vf(folderName, scanVF_URL, chapNumber)

