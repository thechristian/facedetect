import cv2
import os
import os.path
import  glob
# print "Brought together by theChristian"

global ImagesWithFaces
# global url_Images


def identifyFace(imgName):
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')  # load the required trained XML classifiers
    eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
    img = cv2.imread(imgName)  # reading image from source
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # converting image to gray scale

    # detecting faces
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)


    for (x,y,w,h) in faces:
        img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = img[y:y + h, x:x + w]
        eyes = eye_cascade.detectMultiScale(roi_gray)

        if True:
            os.path.join(ImagesWithFaces, img)
        else:
            print "not an image"
        # detecting eyeballs
        for (ex, ey, ew, eh) in eyes:
             cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)


img_dir = "url_Images"
data_path = os.path.join(img_dir, '*g')
#files = glob.glob(data_path)
# data = []
#for f1 in files:
#    identifyFace(f1)
