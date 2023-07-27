import cv2
import glob

globs = glob.glob("*.jpg")


for image in globs: 
    im = cv2.imread(image)
    resized_img = cv2.resize(im, (100, 100))
    cv2.imwrite("resized_{}".format(image.split("/")[-1]), resized_img)


