import requests
import sys
import shutil
import os
from PIL import Image


def findExtention(URLpreformated: str, chapNumber: int, pageNumber: int) -> str:
    """
    Function that find the correct extention whiting the knows one

    -----
    Parameters:
    - An string preformated with three "{}"
    It use the format methode to check the extetion
    - chapitre number
    - page number

    -----
    Retrurn: the format of the extetion after the final point (eg: jpg, png, ...)
    """
    extentionType = "jpg"
    testURL = URLpreformated.format(chapNumber, pageNumber, extentionType)
    resp = requests.get(testURL)
    if(resp.status_code == 200):
        return extentionType
    else:
        extentionType = "png"
        testURL = URLpreformated.format(chapNumber, pageNumber, extentionType)
        resp = requests.get(testURL)
        if(resp.status_code == 200):
            return extentionType
        else:
            extentionType = "JPG"
            testURL = URLpreformated.format(chapNumber, pageNumber, extentionType)
            resp = requests.get(testURL)
            if(resp.status_code == 200):
                return extentionType
            else:
                extentionType = "jpeg"
                testURL = URLpreformated.format(chapNumber, pageNumber, extentionType)
                resp = requests.get(testURL)
                if(resp.status_code == 200):
                    return extentionType
                else:
                    return "none"


def findScanURL(scanVF_URL: str, chapNumber: int, pageNumber: int) -> (bool, str, str):
    """
    Function to find the working URL for a chapter

    -----
    Parameter: the scan-vf URL that never change
    
    -----
    Returns:
    - boolean for the validity of the request
    - final good preformated url
    - extention
    """
    #First know URL type
    preformatedURL = scanVF_URL + "chapitre-{}/{:02d}.{}"
    extentionTyoe = findExtention(preformatedURL, chapNumber, pageNumber)
    if(extentionTyoe == "none"):
        #second known URL type
        preformatedURL = scanVF_URL + "{}/{:02d}.{}"
        extentionTyoe = findExtention(preformatedURL, chapNumber, pageNumber)
        if(extentionTyoe == "none"):
            #third known URL type
            preformatedURL = scanVF_URL + "chapitre-{}/%20({}).{}"
            extentionTyoe = findExtention(preformatedURL, chapNumber, pageNumber)
            if(extentionTyoe == "none"):
                return False, preformatedURL, extentionTyoe

    return True, preformatedURL, extentionTyoe


# cheching for arguments
if(len(sys.argv) > 1):
    if(int(sys.argv[1]) >= 0):
        chapNumber = int(sys.argv[1]) - 1
    else:
        chapNumber = 0
else:
    chapNumber = 0

# TODO: change folder name according to the scan
folderName = "One_Piece"
scanVF_URL = "https://www.scan-vf.co/uploads/manga/one_piece/chapters/"


try:
    os.mkdir("./" + folderName)
except:
    print("Warning: File {} already exist".format(folderName))


try:
    while(True):
        pageNumber = 0
        chapNumber += 1
        extentionType = "jpg"

        path = "./{}/Chap_{}".format(folderName, chapNumber)

        try:
            os.mkdir(path)
        except FileExistsError:
            print("Error: File {} already exist".format(path))
            break

        
        # Checking if the chapter exist according to all the known URLs
        isChapter, correctURL, extentionType = findScanURL(scanVF_URL, chapNumber, 1)

        if(not isChapter):
            break
        

        while (True):
            pageNumber += 1

            # This is the image url.
            image_url = correctURL.format(chapNumber, pageNumber, extentionType)
            resp = requests.get(image_url, stream=True)
            if(resp.status_code != 200):
                extentionType = findExtention(correctURL, chapNumber, pageNumber)
                image_url = correctURL.format(chapNumber, pageNumber, extentionType)
                resp = requests.get(image_url, stream=True)
                if(resp.status_code != 200):
                    break


            
            # Open a local file with wb ( write binary ) permission.
            name = path + "/{}_{:02d}.jpg".format(chapNumber, pageNumber)

            
            resp.raw.decode_content = True

            im = Image.open(resp.raw) 

            if(extentionType == "jpg"):
                try:
                    im.save(name)
                except:
                    rgb_im = im.convert('RGB')
                    rgb_im.save(name)
            else:
                rgb_im = im.convert('RGB')
                rgb_im.save(name)

            del resp

except KeyboardInterrupt:
    pass
