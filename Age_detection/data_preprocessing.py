import os
import cv2 as cv
from tqdm import tqdm
FILE_PATH = "/home/sacreds/Downloads/FGNET/images/"
TRAIN_PATH = "/home/sacreds/Documents/GitHub/StudyMonk-ml-tests/OpenCV-StudyMonk/Age_detection/main_data/train/images"
TEST_PATH = "/home/sacreds/Documents/GitHub/StudyMonk-ml-tests/OpenCV-StudyMonk/Age_detection/main_data/test/images"
files = os.listdir(FILE_PATH)
files.sort()
# print(files)
for file in tqdm(files):
    ages = [str(x) for x in range(15,65)]
    img = cv.imread(FILE_PATH+"/"+file)
    img = cv.cvtColor(img,cv.COLOR_BGR2RGB)
    img = cv.resize(img,(128,128))
    for age in ages:
        if file.endswith(age+".JPG") or file.endswith(age+"a.JPG") or file.endswith(age+"b.JPG"):
            path = "{}/{}".format(TEST_PATH,file)
            path3 = "{}/{}".format(TRAIN_PATH,file)
            cv.imwrite(path,img)
            os.remove(path3)
            # os.system("cp {}/{} {}".format(FILE_PATH,file,TEST_PATH))
        
        else:
            path2 = "{}/{}".format(TRAIN_PATH,file)
            cv.imwrite(path2,img)
            # os.system("cp {}/{} {}".format(FILE_PATH,file,TRAIN_PATH))