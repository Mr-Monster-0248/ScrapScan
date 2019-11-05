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
print("Stop with ctrl+c")
ssvf.scrapScan_vf(folderName, scanVF_URL)

