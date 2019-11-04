import requests
import sys
import shutil
import os

scrap = True

# cheching for arguments
if(len(sys.argv) > 1):
    chapNumber = int(sys.argv[1]) - 1
else:
    chapNumber = 0

# TODO: change folder name according to the scan
folderName = "One_Piece"
scanVF_URL = "https://www.scan-vf.co/uploads/manga/one_piece/chapters/"

if(chapNumber == 0):
    try:
        os.mkdir("./" + folderName)
    except:
        print("File already exist")
        scrap = False


while(scrap):

    pageNumber = 0
    chapNumber += 1

    path = "./{}/Chap_{}".format(folderName, chapNumber)

    os.mkdir(path)

    # URL image test (nombre chapitre total)
    test_fin = "https://www.scan-vf.co/uploads/manga/one_piece/chapters/chapitre-" + \
        str(chapNumber) + "/01.jpg"

    resp = requests.get(test_fin, stream=True)

    if(resp.status_code != 200):
        test_fin = "https://www.scan-vf.co/uploads/manga/one_piece/chapters/chapitre-" + \
            str(chapNumber) + "/01.png"
        resp = requests.get(test_fin, stream=True)
        if(resp.status_code != 200):
            test_fin = "https://www.scan-vf.co/uploads/manga/one_piece/chapters/" + \
                str(chapNumber) + "/01.jpg"
            resp = requests.get(test_fin, stream=True)
            if(resp.status_code != 200):
                break

    while (True):

        isjpg = True
        pageNumber += 1

        # This is the image url.
        image_url = "{}chapitre-{}/{:02d}.jpg".format(
            scanVF_URL, chapNumber, pageNumber)

        # Test de la request avec .jpg
        resp = requests.get(image_url, stream=True)
        if(resp.status_code != 200):
            isjpg = False
            image_url = "{}chapitre-{}/{:02d}.png".format(
                scanVF_URL, chapNumber, pageNumber)

            # Test de la request avec .png
            resp = requests.get(image_url, stream=True)
            if(resp.status_code != 200):
                isjpg = True
                image_url = "{}{}/{:02d}.jpg".format(
                    scanVF_URL, chapNumber, pageNumber)

                # Test de la request avec url differente connue TODO: ajouter les autres type d'URL
                resp = requests.get(image_url, stream=True)
                if(resp.status_code != 200):
                    break  # Page introuvable chapitre suivant

        # Open a local file with wb ( write binary ) permission.
        name = path + \
            "/{}_{:02d}.{}".format(chapNumber, pageNumber,
                                   "jpg" if isjpg else "png")

        local_file = open(name, 'wb')
        resp.raw.decode_content = True
        shutil.copyfileobj(resp.raw, local_file)

        del resp
