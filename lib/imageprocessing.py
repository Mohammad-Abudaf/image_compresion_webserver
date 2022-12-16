import numpy as np
from matplotlib import pyplot as plt
from matplotlib.image import imsave
from matplotlib.image import imread
from scipy.signal import convolve2d
from lib.kernels import *
from mpl_toolkits.mplot3d import axes3d
import cv2


class ImageProcessing:
    @staticmethod
    def cap_image():
        cam = cv2.VideoCapture(0)

        cv2.namedWindow("test")

        img_counter = 0

        while True:
            ret, frame = cam.read()
            if not ret:
                print("failed to grab frame")
                break
            cv2.imshow("test", frame)

            k = cv2.waitKey(1)
            if k % 256 == 27:
                # ESC pressed
                print("Escape hit, closing...")
                break
            elif k % 256 == 32:
                # SPACE pressed
                img_name = "assets/opencv_frame_{}.jpg".format(0)
                cv2.imwrite(img_name, frame)
                print("{} written!".format(img_name))
                img_counter += 1

        cam.release()

        cv2.destroyAllWindows()

    @staticmethod
    def compress(img_path, ratio):
        A = imread(img_path)
        B = np.mean(A, -1)
        Bt = np.fft.fft2(B)
        Btsotred = np.sort(np.abs(Bt.reshape(-1)))
        keep = ratio
        threshold = Btsotred[int(np.floor((1 - keep) * len(Btsotred)))]
        index = np.abs(Bt) > threshold
        AtLow = Bt * index
        Alow = np.fft.ifft2(AtLow).real
        imsave("assets/resultImg.jpg", Alow, cmap="gray")

    @staticmethod
    def visualize_image(img_path):
        A = imread(img_path)
        B = np.mean(A, -1)
        plt.rcParams['figure.figsize'] = [6, 6]
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        x, y = np.meshgrid(np.arange(1, np.shape(B)[1]+1), np.arange(1, np.shape(B)[0]+1))
        ax.plot_surface(x[0::10, 0::10], y[0::10, 0::10], 256 - B[0::10, 0::10], cmap="viridis", edgecolor='none')
        ax.set_title("Surface plot")
        ax.mouse_init()
        ax.view_init(200, 270)
        plt.show()
