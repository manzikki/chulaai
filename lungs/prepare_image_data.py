#create a image - label mapping out of Data_Entry_2017_v2020.csv
#Iterate over images, convert them to 128 x 128 byte arrays
#create a file lung_c.csv that contains the image data 16384 columns + no illness = 0, illness = 1
import os, sys
import PIL.Image
import csv
import io
import cv2

if not hasattr(PIL.Image, 'Resampling'):  # Pillow<9.0
    PIL.Image.Resampling = PIL.Image

images_labels = {}
with open('Data_Entry_2017_v2020.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    rowno = 0
    for row in csv_reader:
        rowno += 1
        if rowno > 1:
            if "No Finding" in row[1]:
                images_labels[row[0]] = 0
            else:
                images_labels[row[0]] = 1

#convert each image
dir_list = os.listdir(".")
for fitem in dir_list:
    if "png" in fitem and fitem in images_labels:
        print(fitem)
        size = 128, 128
        outfile = "small-" + fitem
        im = PIL.Image.open(fitem)
        im.thumbnail(size, PIL.Image.Resampling.LANCZOS)
        im.save(outfile)
        #open again and get the bytes
        img = cv2.imread(outfile)
        img_bytes = img.tobytes()
        bytestr = ""
        for i in img_bytes:
            bytestr = bytestr + str(int(i))+","
        #add the label
        label = images_labels[fitem]
        bytestr = bytestr + str(label) + "\n"
        #img_str = cv2.imencode('.jpg', img)[1].tostring()
        #>>> nparr = np.fromstring(STRING_FROM_DATABASE, np.uint8)
        #>>> img = cv2.imdecode(nparr, cv2.CV_LOAD_IMAGE_COLOR)
        #print(img_str)
        outfile2 = "lung_c.csv"
        of2 = open(outfile2, 'a')
        of2.write(bytestr)
        os.remove(outfile)
