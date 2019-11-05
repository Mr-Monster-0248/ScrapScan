from PIL import Image
import sys
import os


# cheching for arguments
if(len(sys.argv) > 1):
    if(int(sys.argv[1]) > 0):
        chapNumber = int(sys.argv[1]) - 1
    else:
        chapNumber = 0
else:
    chapNumber = 435

try:
    os.mkdir("./pdf")
except:
    print("Warning: File ./pdf already exist")

while(True):

    chapNumber = chapNumber + 1
    name = "./One_Piece/Chap_{}/{}_01.jpg".format(chapNumber, chapNumber)

    title = "One Piece Chapitre {}".format(chapNumber)
    saveAs = "./pdf/One_Piece_Chap_{}.pdf".format(chapNumber)


    try:
        local_file = open(name, 'r')
    except:
        break

    pageNumber = 0
    imagesArray = []

    while(True):

        pageNumber += 1
        name = "./One_Piece/Chap_{}/{}_{:02d}.jpg".format(chapNumber, chapNumber, pageNumber)

        try:
            imagesArray.append(Image.open(name))
        except:
            break

    
    imagesArray[0].save(saveAs, save_all=True, append_images=imagesArray[1:], author="Eiichiro Oda", title=title)

    for i in range(len(imagesArray)):
        imagesArray[i].close()
