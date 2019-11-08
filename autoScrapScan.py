import scrap_scan_vf as ssvf
import scangetter
import jpgtopdf as toPDF

# the only url working for now
myURL = "https://www.scan-vf.co/"

choiceNames, choiceURL = scangetter.searchScan(myURL)
choice = scangetter.userChoice(choiceNames)

folderName = choiceNames[choice]
preformatURL = "https://www.scan-vf.co/uploads/manga/{}/chapters/"
scanVF_URL =  preformatURL.format(choiceURL[choice])

print("Scraping for", folderName)

try:
    chapNumber = int(input("Chapter to start(0 default): ")) -1
except:
    chapNumber = 0

print("Stop with ctrl+c")
ssvf.scrapScan_vf(folderName, scanVF_URL, chapNumber)

choice = input("Do you want to transform your chapters into pdf ? [y/n] (default n): ")
if(choice == 'y' or choice == 'Y'):
    author = input("Enter the autor to save (default none): ")
    toPDF.toPDF(folderName, chapNumber, author)

