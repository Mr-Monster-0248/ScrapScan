import requests
import sys
import shutil
import os
from PIL import Image

scrap = True

# cheching for arguments
if(len(sys.argv) > 1):
    if(int(sys.argv[1]) > 0):
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
    while(scrap):
        pageNumber = 0
        chapNumber += 1

        path = "./{}/Chap_{}".format(folderName, chapNumber)

        try:
            os.mkdir(path)
        except FileExistsError:
            print("Error: File {} already exist".format(path))
            break

        # URL image test (nombre chapitre total)
        test_fin = "{}chapitre-{}/01.jpg".format(scanVF_URL, chapNumber)

        resp = requests.get(test_fin, stream=True)

        if(resp.status_code != 200):
            test_fin = "{}chapitre-{}/01.png".format(scanVF_URL, chapNumber)
            resp = requests.get(test_fin, stream=True)
            if(resp.status_code != 200):
                test_fin = "{}{}/01.jpg".format(scanVF_URL, chapNumber)
                resp = requests.get(test_fin, stream=True)
                if(resp.status_code != 200):
                    test_fin = "{}chapitre-{}/01.JPG".format(scanVF_URL, chapNumber)
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

                    # Test de la request avec url differente(sans Chapitre-) connue
                    resp = requests.get(image_url, stream=True)
                    if(resp.status_code != 200):
                        image_url = "{}chapitre-{}/{:02d}.JPG".format(
                            scanVF_URL, chapNumber, pageNumber)

                        # Test de la request avec url differente(JPG MAJ) connue TODO: ajouter les autres type d'URL
                        resp = requests.get(image_url, stream=True)
                        if(resp.status_code != 200):
                            break  # Page introuvable chapitre suivant

            # Open a local file with wb ( write binary ) permission.
            name = path + "/{}_{:02d}.jpg".format(chapNumber, pageNumber)

            
            resp.raw.decode_content = True

            if(isjpg):
                im = Image.open(resp.raw)
                im.save(name)
            else:
                im = Image.open(resp.raw)
                rgb_im = im.convert('RGB')
                rgb_im.save(name)

            del resp

except KeyboardInterrupt:
    pass