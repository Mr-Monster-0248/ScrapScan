from PIL import Image
import sys
import os

def toPDF(directoryName:str, chapNumber:str, author = ""):
    """
    Function to transform chapter into PDFs
    """
    while(True):

        chapNumber += 1
        name = "./{}/Chap_{}/{}_01.jpg".format(directoryName, chapNumber, chapNumber)

        title = "{} Chapitre {}".format(directoryName, chapNumber)
        saveAs = "./pdf/{} Chap {}.pdf".format(directoryName, chapNumber)


        try:
            local_file = open(name, 'r')
        except:
            print("Chapter", chapNumber, "not found exiting...")
            break

        pageNumber = 0
        imagesArray = []

        while(True):

            pageNumber += 1
            name = "./{}/Chap_{}/{}_{:02d}.jpg".format(directoryName, chapNumber, chapNumber, pageNumber)

            try:
                imagesArray.append(Image.open(name))
            except:
                break

        
        imagesArray[0].save(saveAs, save_all=True, append_images=imagesArray[1:], author=author, title=title)

        for i in range(len(imagesArray)):
            imagesArray[i].close()


if __name__ == "__main__":
    # cheching for arguments
    if(len(sys.argv) > 1):
        if(int(sys.argv[1]) > 0):
            chapNumber = int(sys.argv[1]) - 1
        else:
            chapNumber = 0
    else:
        chapNumber = 0

    try:
        os.mkdir("./pdf")
    except:
        print("Warning: File ./pdf already exist")

    toPDF("One_piece", chapNumber, "Echiiro Oda")
