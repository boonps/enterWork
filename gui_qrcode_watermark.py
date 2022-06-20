import cv2
import matplotlib.pyplot as plt
import cv2 as cv
import numpy as np


def image_resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]
    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image
    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)
    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation=inter)
    # return the resized image
    return resized


cap = cv.VideoCapture(0)
img_path = 'NULOGO.png'
logo = cv2.imread(img_path, -1)
watermark = image_resize(logo, height=100)
watermark = cv2.cvtColor(watermark, cv2.COLOR_BGR2BGRA)

if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
    frame_h, frame_w, frame_c = frame.shape
    # overlay with 4 channels BGR and Alpha
    overlay = np.zeros((frame_h, frame_w, 4), dtype='uint8')
    watermark_h, watermark_w, watermark_c = watermark.shape
    # replace overlay pixels with watermark pixel values
    for i in range(0, watermark_h):
        for j in range(0, watermark_w):
            if watermark[i, j][3] != 0:
                offset = 10
                h_offset = frame_h - watermark_h - offset
                w_offset = frame_w - watermark_w - offset
                overlay[h_offset + i, w_offset + j] = watermark[i, j]

    cv2.addWeighted(overlay, 1, frame, 1, 0, frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # Display the resulting frame
    cv2.line(frame, (200, 200), (300, 200), (0, 206, 250), 5)  # x y
    cv2.line(frame, (200, 200), (200, 300), (0, 206, 250), 5)  # x y-------1

    cv2.line(frame, (800, 200), (700, 200), (0, 206, 250), 5)  # x y
    cv2.line(frame, (800, 200), (800, 300), (0, 206, 250), 5)  # x y-------2

    cv2.line(frame, (200, 600), (200, 500), (0, 206, 250), 5)  # x y
    cv2.line(frame, (200, 600), (300, 600), (0, 206, 250), 5)  # x y-------3

    cv2.line(frame, (800, 600), (800, 500), (0, 206, 250), 5)  # x y
    cv2.line(frame, (800, 600), (700, 600), (0, 206, 250), 5)  # x y-------4

    # Title
    cv2.putText(frame, 'DTT Check IN', (100, 100), cv2.FONT_HERSHEY_DUPLEX, 4, (0, 0, 0), 2, cv2.LINE_AA)

    # plt.imshow(frame)
    # plt.show()
    # cv2.imshow("Frames", frame)

    cv.imshow('frame', frame)
    # cv.imshow('frame', watermark)
    if cv.waitKey(1) == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv.destroyAllWindows()
