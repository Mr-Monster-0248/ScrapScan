from fpdf import FPDF

chap = 0

while(True):

    chap = chap + 1
    name = "./testpdf/Chap_" + str(chap) + "/" + str(chap) + "_01.jpg"

    try:
        local_file = open(name, 'r')
    except:
        break

    page = 0

    pdf = FPDF()

    while(True):
        page = page + 1
        
        if (page < 10):
            name = "./testpdf/Chap_" + str(chap) + "/" + str(chap) + "_0" + str(page) + ".jpg"
        else:
            name = "./testpdf/Chap_" + str(chap) + "/" + str(chap) + "_" + str(page) + ".jpg"

        try:
            local_file = open(name, 'r')
        except:
            break

        pdf.add_page()
        pdf.image(name,0,0,210,297)
    
    outputname = "./testpdf/One_Piece_Chap_" + str(chap) + ".pdf"
    pdf.output(outputname, "F")

