import requests
import sys
import shutil
import os
from PIL import Image
from termcolor import colored


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
    if resp.status_code == 200:
        return extentionType
    else:
        extentionType = "png"
        testURL = URLpreformated.format(chapNumber, pageNumber, extentionType)
        resp = requests.get(testURL)
        if resp.status_code == 200:
            return extentionType
        else:
            extentionType = "JPG"
            testURL = URLpreformated.format(chapNumber, pageNumber, extentionType)
            resp = requests.get(testURL)
            if resp.status_code == 200:
                return extentionType
            else:
                extentionType = "jpeg"
                testURL = URLpreformated.format(chapNumber, pageNumber, extentionType)
                resp = requests.get(testURL)
                if resp.status_code == 200:
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
    # First know URL type
    preformatedURL = scanVF_URL + "chapitre-{}/{:02d}.{}"
    extentionTyoe = findExtention(preformatedURL, chapNumber, pageNumber)
    if extentionTyoe == "none":
        # second known URL type
        preformatedURL = scanVF_URL + "{}/{:02d}.{}"
        extentionTyoe = findExtention(preformatedURL, chapNumber, pageNumber)
        if extentionTyoe == "none":
            # third known URL type
            preformatedURL = scanVF_URL + "chapitre-{}/%20({:02}).{}"
            extentionTyoe = findExtention(preformatedURL, chapNumber, pageNumber)
            if extentionTyoe == "none":
                # forth known URL type
                preformatedURL = scanVF_URL + "chapitre-{}/{:02}_" + "{:02}".format(pageNumber + 1) + ".{}"
                extentionTyoe = findExtention(preformatedURL, chapNumber, pageNumber)
                if extentionTyoe == "none":
                    # forth known URL type
                    preformatedURL = scanVF_URL + "chapitre-{}/{:02}-" + \
                                     "{:02}".format(pageNumber + 1) + ".{}"
                    extentionTyoe = findExtention(
                        preformatedURL, chapNumber, pageNumber)
                    if extentionTyoe == "none":
                        return False, preformatedURL, extentionTyoe

    return True, preformatedURL, extentionTyoe


def scrapScan_vf(folderName, scanVF_URL, chapNumber=0):
    try:
        os.mkdir("./" + folderName)
    except:
        print(colored("Warning:", "yellow"), "File {} already exist".format(folderName))

    failedAttempt = 0
    pageNumber = 0

    try:
        while True:
            chapNumber += 1
            extentionType = "jpg"

            # DEBUG: print("testing for chapter", chapNumber, "and page", pageNumber)
            # Checking if the chapter exist according to all the known URLs
            isChapter, correctURL, extentionType = findScanURL(scanVF_URL, chapNumber, pageNumber)

            if not isChapter:
                failedAttempt += 1
                # DEBUG: print("Failled reaching for chapter", chapNumber, "attempt:", failedAttempt)
                chapNumber -= 1
                pageNumber += 1
                if (failedAttempt > 3):
                    print(colored("Error:", "red"), "Could not find chapter", chapNumber, "Exiting...")
                    break
            else:
                path = "./{}/Chap_{}".format(folderName, chapNumber)

                if os.path.isdir(path):
                    print(colored("Warning:", "yellow"), path, "will be override")
                    shutil.rmtree(path)
                    os.mkdir(path)
                else:
                    os.mkdir(path)

                while (True):

                    # This is the image url.
                    image_url = correctURL.format(chapNumber, pageNumber, extentionType)
                    resp = requests.get(image_url, stream=True)
                    if resp.status_code != 200:  # extention type might have change during page scraping
                        extentionType = findExtention(correctURL, chapNumber, pageNumber)
                        image_url = correctURL.format(chapNumber, pageNumber, extentionType)
                        resp = requests.get(image_url, stream=True)
                        if resp.status_code != 200:  # url might have change during page scraping (very unlikely)
                            isChapter, correctURL, extentionType = findScanURL(
                                scanVF_URL, chapNumber, pageNumber)
                            image_url = correctURL.format(
                                chapNumber, pageNumber, extentionType)
                            resp = requests.get(image_url, stream=True)
                            if not isChapter:
                                # DEBUG: print(colored("Error:", "red"), "at chapter",  chapNumber, "at page", pageNumber)
                                failedAttempt += 1
                                pageNumber += 1

                    if failedAttempt > 1:
                        output = "Finished chapter: {}".format(chapNumber)
                        print(colored(output, "green"))
                        failedAttempt = 0
                        pageNumber = 0
                        break

                    if isChapter:
                        failedAttempt = 0

                        # Open a local file with wb ( write binary ) permission.
                        name = path + "/{}_{:02d}.jpg".format(chapNumber, pageNumber)

                        pageNumber += 1
                        resp.raw.decode_content = True

                        im = Image.open(resp.raw)

                        if extentionType == "jpg":
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


if __name__ == "__main__":

    # cheching for arguments
    if len(sys.argv) > 1:
        if int(sys.argv[1]) >= 0:
            chapNumber = int(sys.argv[1]) - 1
        else:
            chapNumber = 0
    else:
        chapNumber = 0

    # TODO: change folder name according to the scan
    folderName = "One_Piece"
    scanVF_URL = "https://www.scan-vf.co/uploads/manga/one_piece/chapters/"

    scrapScan_vf(folderName, scanVF_URL, chapNumber)
