#
#
#     # Display the resulting frame
#     cv2.line(frame, (200, 200), (300, 200), (0, 206, 250), 5)  # x y
#     cv2.line(frame, (200, 200), (200, 300), (0, 206, 250), 5)  # x y-------1
#
#     cv2.line(frame, (800, 200), (700, 200), (0, 206, 250), 5)  # x y
#     cv2.line(frame, (800, 200), (800, 300), (0, 206, 250), 5)  # x y-------2
#
#     cv2.line(frame, (200, 600), (200, 500), (0, 206, 250), 5)  # x y
#     cv2.line(frame, (200, 600), (300, 600), (0, 206, 250), 5)  # x y-------3
#
#     cv2.line(frame, (800, 600), (800, 500), (0, 206, 250), 5)  # x y
#     cv2.line(frame, (800, 600), (700, 600), (0, 206, 250), 5)  # x y-------4
#
#     # Title
#     cv2.putText(frame, 'DTT Check IN', (100, 100), cv2.FONT_HERSHEY_DUPLEX, 4, (0, 0, 0), 2, cv2.LINE_AA)
#
#     # plt.imshow(frame)
#     # plt.show()
#     # cv2.imshow("Frames", frame)
#     cv2.imshow('Frame', logo)
#     # cv.imshow('Frame', img1)
#     # cv.imshow('frame', watermark)
#     if cv.waitKey(1) == ord('q'):
#         break
# # When everything done, release the capture
# # cv2.imshow('Frame', img1)
# cap.release()
# cv.destroyAllWindows()

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtWidgets
import sys


def window():
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setGeometry(0, 0, 900, 800)
    window.setWindowTitle("DTT Check IN")
    window.show()
    sys.exit(app.exec_())


window()
