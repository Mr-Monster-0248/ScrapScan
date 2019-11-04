import requests
import shutil
import os

# Chap debut - 1
y = 245

# Changer nom manga
#os.mkdir("./One_Piece")

while (True):

    z = 0
    y = y + 1

    path = "./One_Piece/Chap_" + str(y)

    os.mkdir(path)

    # URL image test (nombre chapitre total)
    test_fin = "https://www.scan-vf.co/uploads/manga/one_piece/chapters/chapitre-" + str(y) + "/01.jpg"
    

    resp = requests.get(test_fin, stream=True)
        
    if(resp.status_code != 200):
        test_fin = "https://www.scan-vf.co/uploads/manga/one_piece/chapters/chapitre-" + str(y) + "/01.png"
        resp = requests.get(test_fin, stream=True)
        if(resp.status_code != 200):
            break



    while (True):
        
        z = z + 1

        # This is the image url.
        if(z<10):
            image_url = "https://www.scan-vf.co/uploads/manga/one_piece/chapters/chapitre-" + str(y) + "/0" + str(z) +".jpg"
        
        else:
            image_url = "https://www.scan-vf.co/uploads/manga/one_piece/chapters/chapitre-" + str(y) + "/" + str(z) +".jpg"

        # Open the url image, set stream to True, this will return the stream content.
        resp = requests.get(image_url, stream=True)
        
        if(resp.status_code != 200):
            if(z<10):
                image_url = "https://www.scan-vf.co/uploads/manga/one_piece/chapters/chapitre-" + str(y) + "/0" + str(z) +".png"
        
            else:
                image_url = "https://www.scan-vf.co/uploads/manga/one_piece/chapters/chapitre-" + str(y) + "/" + str(z) +".png"

            resp = requests.get(image_url, stream=True)
            if(resp.status_code != 200):
                break

        # Open a local file with wb ( write binary ) permission.
        if(z<10):
            name = path + "\\" + str(y) + "_0" + str(z) + ".jpg"
        else:
            name = path + "\\" + str(y) + "_" + str(z) + ".jpg"

        local_file = open(name, 'wb')

        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        resp.raw.decode_content = True

        # Copy the response stream raw data to local image file.
        shutil.copyfileobj(resp.raw, local_file)

        # Remove the image url response object.
        del resp
    



