import cv2
import matplotlib.pyplot as plt
import argparse
import os

# parser = argparse.ArgumentParser()
# parser.add_argument("--img",required=True,type=str,help="Path of Image For splitting Colors")

# args = parser.parse_args()
# file_img = args.img
def split_channels(file_img):
    img = cv2.imread(file_img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    print('Shape of input image --> ', img.shape)

    r, g, b = cv2.split(img)

    os.makedirs('results',exist_ok=True)
    print('Shape of red channel --> ', r.shape)
    print('Shape of green channel --> ', g.shape)
    print('Shape of blue channel --> ', b.shape)

    os.makedirs("results",exist_ok=True)
    images = [cv2.merge((r, g, b)), r, g, b]

    plt.subplot(2, 2, 1)
    plt.xticks([])
    plt.yticks([])
    plt.imshow(images[0])
    plt.title('original')


    plt.subplot(2, 2, 2)
    plt.xticks([])
    plt.yticks([])
    plt.imshow(images[1], cmap='Reds')
    plt.title('red')

    plt.subplot(2, 2, 3)
    plt.xticks([])
    plt.yticks([])
    plt.imshow(images[2], cmap='Greens')
    plt.title('green')


    plt.subplot(2, 2, 4)
    plt.xticks([])
    plt.yticks([])
    plt.imshow(images[3], cmap='Blues')
    plt.title('blue')
    plt.savefig('results/result_img.png')

    print("Image Saved")

# plt.show()